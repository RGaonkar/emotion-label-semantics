from pathlib import Path
import numpy as np
import torch
from ..common.tools import logger
import pickle

class ModelCheckpoint(object):
    """Save the model after every epoch.
    # Arguments
        checkpoint_dir: string, path to save the model file.
        monitor: quantity to monitor.
        verbose: verbosity mode, 0 or 1.
        save_best_only: if `save_best_only=True`,
            the latest best model according to
            the quantity monitored will not be overwritten.
        mode: one of {auto, min, max}.
            If `save_best_only=True`, the decision
            to overwrite the current save file is made
            based on either the maximization or the
            minimization of the monitored quantity. For `val_acc`,
            this should be `max`, for `val_loss` this should
            be `min`, etc. In `auto` mode, the direction is
            automatically inferred from the name of the monitored quantity.
    """
    def __init__(self, checkpoint_dir,
                 monitor,
                 arch,
                 mode='min',
                 epoch_freq=1,
                 best = None,
                 save_best_only = True):

        if isinstance(checkpoint_dir,Path):
            checkpoint_dir = checkpoint_dir
        else:
            checkpoint_dir = Path(checkpoint_dir)
        assert checkpoint_dir.is_dir()
        checkpoint_dir.mkdir(exist_ok=True)
        self.base_path = checkpoint_dir
        self.arch = arch
        self.monitor = monitor
        self.epoch_freq = epoch_freq
        self.save_best_only = save_best_only

        # 计算模式
        if mode == 'min':
            self.monitor_op = np.less
            self.best = np.Inf

        elif mode == 'max':
            self.monitor_op = np.greater
            self.best = -np.Inf
        # 这里主要重新加载模型时候
        #对best重新赋值
        if best:
            self.best = best

        if save_best_only:
            self.model_name = f"BEST_{arch}_MODEL.pth"

    def epoch_step(self, state,current):
        '''
        :param state: 需要保存的信息
        :param current: 当前判断指标
        :return:
        '''
        if self.save_best_only:
            ##apply the np.less function on the selected metric
            ##if the mmetric for the current epoch is less than that seen for the other epochs, update the best metric value
            print ("Metric for current epoch:")
            print (current)
            print ("Best metric so far:")
            print (self.best)

            if self.monitor_op(current, self.best):

                logger.info(f"\nEpoch {state['epoch']}: {self.monitor} improved from {self.best:.5f} to {current:.5f}")
                self.best = current
                print ("Updated best:")
                print (self.best)

                state['best'] = self.best
                best_path = self.base_path/ self.model_name
                
                torch.save(state, str(best_path))

            print ("                        ")
            print ("------------------------")

        else:
            filename = self.base_path / f"epoch_{state['epoch']}_{state[self.monitor]}_{self.arch}_model.bin"
            if state['epoch'] % self.epoch_freq == 0:
                logger.info(f"\nEpoch {state['epoch']}: save model to disk.")
                torch.save(state, str(filename))

    def bert_epoch_step(self, state,current):
        model_to_save = state['model']

        if self.save_best_only:

            print ("Saving the best model:")
            if self.monitor_op(current, self.best):
                print ("Based on the criteria:")
                logger.info(f"\nEpoch {state['epoch']}: {self.monitor} improved from {self.best:.5f} to {current:.5f}")
                self.best = current
                state['best'] = self.best
                print (self.base_path)
                
                print ("Saving the model:")
                model_to_save.save_pretrained(str(self.base_path))

                output_config_file = self.base_path / 'config.json'
                
                print ("Saving the config file:")
                with open(str(output_config_file), 'w') as f:
                    f.write(model_to_save.config.to_json_string())

                state.pop("model")
                
                print ("Saving the model state:")                
                torch.save(state,self.base_path / 'checkpoint_info.bin')

                print ("Saving the predicted labels:")
                ##Save the predicted labels from the training set
                pickle.dump(state['val_predicted'], open(self.base_path / "val_predicted.p", "wb"))

                print ("Saving the true labels:")
                ##Save the true labels from the training set
                pickle.dump(state['val_true'], open(self.base_path / "val_true.p", "wb"))

                print ("Saving the true train labels:")
                pickle.dump(state['train_true'], open(self.base_path / "train_true.p", "wb"))

#                print("Saving the label graph from the model:")
#                pickle.dump(state['label_graph'], open(self.base_path / "label_graph.p", "wb"))


        else:
            if state['epoch'] % self.epoch_freq == 0:
                save_path = self.base_path / f"checkpoint-epoch-{state['epoch']}"
                save_path.mkdir(exist_ok=True)
                logger.info(f"\nEpoch {state['epoch']}: save model to disk.")
                model_to_save.save_pretrained(save_path)
                output_config_file = save_path / 'config.json'
        
                with open(str(output_config_file), 'w') as f:
                    f.write(model_to_save.config.to_json_string())
                state.pop("model")
                torch.save(state, save_path / 'checkpoint_info.bin')
