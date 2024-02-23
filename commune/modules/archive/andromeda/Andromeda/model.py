import torch 
from torch.nn import Module
import bitsandbytes
from Andromeda.optimus_prime import TransformerWrapper, AutoregressiveWrapper, AndromedaEmbedding, Decoder
from transformers import AutoTokenizer

class AndromedaTokenizer:
    def __init__(self):
        self.tokenizer= AutoTokenizer.from_pretrained(
            "EleutherAI/gpt-neox-20b",
            eos_token="<eos>",
            pad_token="<pad>",
            extra_ids=0,
            model_max_length=8192
        )

    def tokenize_texts(self, texts):
        return self.tokenizer(texts, return_tensors='pt', padding=True, truncation=True).input_ids


class Andromeda(Module):
    """
    Andromeda is a transformer-based model architecture. It initializes with 
    a TransformerWrapper and AutoregressiveWrapper with default or user-specified parameters.
    """
    def __init__(self, num_tokens=50304, 
                 max_seq_len=8192, 
                 dim=2560, depth=32, 
                 dim_head=128, 
                 heads=24,
                 use_abs_pos_emb=False, 
                 alibi_pos_bias=True, 
                 alibi_num_heads=12, 
                 rotary_xpos=True,
                 attn_flash=True, 
                 deepnorm=True, 
                 shift_tokens=1, 
                 attn_one_kv_head=True, 
                 qk_norm=True, 
                 attn_qk_norm=True, 
                 attn_qk_norm_dim_scale=True, 
                 embedding_provider=AndromedaEmbedding()):
        """
        Initialize the model with specified or default parameters.
        Args:
        - num_tokens: Number of tokens in the vocabulary
        - max_seq_len: Maximum sequence length
        - dim: Dimension of the model
        - depth: Depth of the model
        - dim_head: Dimension of the model head
        - heads: Number of heads
        - use_abs_pos_emb: Whether to use absolute position embedding
        - alibi_pos_bias: Alibi position bias
        - alibi_num_heads: Number of alibi heads
        - rotary_xpos: Rotary position
        - attn_flash: Attention flash
        - deepnorm: Deep normalization
        - shift_tokens: Number of tokens to shift
        - attn_one_kv_head: Attention one key/value head
        - qk_norm: Query-key normalization
        - attn_qk_norm: Attention query-key normalization
        - attn_qk_norm_dim_scale: Attention query-key normalization dimension scale
        - embedding_provider: Embedding provider module
        """
        super().__init__()

        try:
            self.andromeda = TransformerWrapper(
                num_tokens=num_tokens,
                max_seq_len=max_seq_len,
                use_abs_pos_emb=use_abs_pos_emb,
                embedding_provider=embedding_provider,
                attn_layers=Decoder(
                    dim=dim,
                    depth=depth,
                    dim_head=dim_head,
                    heads=heads,
                    alibi_pos_bias=alibi_pos_bias,
                    alibi_num_heads=alibi_num_heads,
                    rotary_xpos=rotary_xpos,
                    attn_flash=attn_flash,
                    deepnorm=deepnorm,
                    shift_tokens=shift_tokens,
                    attn_one_kv_head=attn_one_kv_head,
                    qk_norm=qk_norm,
                    attn_qk_norm=attn_qk_norm,
                    attn_qk_norm_dim_scale=attn_qk_norm_dim_scale
                )
            )

            self.decoder = AutoregressiveWrapper(self.andromeda)

        except Exception as e:
            print("Failed to initialize Andromeda: ", e)
            raise

    def forward(self, text_tokens, **kwargs):
        """
        Forward pass through the model. It expects the input text_tokens.
        Args:
        - text_tokens: Input tokens
        - kwargs: Other arguments
        Returns:
        - output from the decoder
        """
        try:
            model_input = self.decoder.forward(text_tokens)[0]
            return self.decoder(model_input, padded_x=model_input[0])
        except Exception as e:
            print("Failed in forward method: ", e)
            raise
