# Project Overview


## Telegram Bot and Model
I used [TinyLlama/TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) for my Telegram Bot. Download the following files and save them in the directory `./TinyLlama`:

- `config.json`
- `generation_config.json`
- `model.safetensors`
- `special_tokens_map.json`
- `tokenizer_config.json`
- `tokenizer.json`
- `tokenizer.model`

Telegram bot address:  https://t.me/My_DSSS_AI_bot

# Project Environment Requirements

## 1. Operating System
- **macOS**: Apple Silicon (M2).

## 2. Python Version
- **Python 3.11**

## 3. Required Python Libraries
Install the following Python libraries using `pip` or `conda`:

### Key Libraries:
- **transformers**: Version `>=4.34` (recommended: 4.48.0).
- **torch**: Version compatible with MPS (Metal Performance Shaders) backend.
- **telegram**: For Telegram Bot interaction.
- **safetensors**: For handling model files.
- **requests**: If downloading model files from cloud storage is required.

## 4. Hardware Requirements
- **Processor**: Apple Silicon M2.
- **Backend**:
  - Use **MPS** (Metal Performance Shaders) for acceleration.
  - Fallback to **CPU** if MPS is unavailable.

## 5. Conda Environment Configuration
Create an `environment.yml` file with the following content:

```yaml
name: hw9
defaults:
  - defaults
  - conda-forge
dependencies:
  - python=3.11
  - pytorch
  - transformers>=4.34
  - telegram
  - safetensors
  - requests
```

### Create the environment:
```bash
conda env create -f environment.yml
```

## 6. Running the Project
Run the main script to start your Telegram bot:
```bash
python hw9.py
```
