
from pathlib import Path
BASE_DIR = Path('pybert')
checkpoints_name = "checkpoints_label_emo_rand"

config = {
    'raw_data_path': BASE_DIR / 'dataset/train_char_label_df.csv',
    'test_path': BASE_DIR / 'dataset/test_char_label_df.csv',
    'data_cache' : BASE_DIR / 'dataset' / checkpoints_name, 
    'data_dir': BASE_DIR / 'dataset',
    'log_dir': BASE_DIR / 'output/log',
    'writer_dir': BASE_DIR / "output/TSboard",
    'figure_dir': BASE_DIR / "output/figure",
    # 'checkpoint_dir': "/home/rgaonkar/context_home/rgaonkar/label_embeddings/code/Bert_Masked_LM/output",
    'checkpoint_dir': BASE_DIR / "output/" / checkpoints_name,
    'cache_dir': BASE_DIR / 'model/',
    'result': BASE_DIR / "output/result",

    'bert_vocab_path': '/home/rgaonkar/context_home/rgaonkar/label_embeddings/code/Bert_Masked_LM/output/random_emotion/model_checkpoint/vocab.txt',
    'bert_config_file': BASE_DIR / 'pretrain/bert/base-uncased/config.json',
    'bert_model_dir': BASE_DIR / 'pretrain/bert/base-uncased',

    'xlnet_vocab_path': BASE_DIR / 'pretrain/xlnet/base-cased/spiece.model',
    'xlnet_config_file': BASE_DIR / 'pretrain/xlnet/base-cased/config.json',
    'xlnet_model_dir': BASE_DIR / 'pretrain/xlnet/base-cased'
}

