from setuptools import setup, find_packages

setup(
  name = 'Andromeda-llm',
  packages = find_packages(exclude=['examples']),
  version = '0.0.3',
  license='MIT',
  description = 'andromeda - Pytorch',
  author = 'Kye Gomez',
  author_email = 'kye@apac.ai',
  url = 'https://github.com/kyegomez/Andromeda',
  long_description_content_type = 'text/markdown',
  keywords = [
    'artificial intelligence',
    'attention mechanism',
    'transformers'
  ],
  install_requires=[
    "torch"
    "lion-pytorch",
    "numpy",
    # colt5_attention
    "einops",
    # local_attention
    "accelerate",
    "transformers",
    # triton
    "SentencePiece",
    "bitsandbytes",
    "datasets",
    "Triton",
    "deepspeed",
    'bitsandbytes'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)