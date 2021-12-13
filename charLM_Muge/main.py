import argparse, random, torch, json, matplotlib, os
import numpy as np
import matplotlib.pyplot as plt
from charlm import CharLM
from common.utils import *
from data import build_data
matplotlib.use('Agg')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   
from train import train


# CONFIG
parser = argparse.ArgumentParser(description='')
args = parser.parse_args()
args.device = 'cuda'
args.batchsize = 128; args.epochs = 10
args.opt= 'Adam'; args.lr = 0.001
args.task = 'lm'
args.seq_to_no_pad = 'surface'

args.trndata = '/home/emrecan/Desktop/NLP/charLM_Muge/data/surf.uniquesurfs.trn.txt'#'models/charlm/data/goldstdsample.tur.trn'
args.valdata = '/home/emrecan/Desktop/NLP/charLM_Muge/data/surf.uniquesurfs.val.txt'#'models/charlm/data/goldstdsample.tur.val'
args.tstdata = args.valdata
args.surface_vocab_file = args.trndata


args.fig, args.axs = plt.subplots(2, sharex=True)
args.plt_style = pstyle = '-'
args.maxtrnsize = 57769 
args.maxvalsize = 8329 
args.maxtstsize = 8517
args.bmodel = 'charlm' 

rawdata, batches, vocab = build_data(args)
trndata, vlddata, tstdata = rawdata
args.trnsize , args.valsize, args.tstsize = len(trndata), len(vlddata), 0
# logging
args.modelname = 'models/'+args.bmodel+'/logs/'+str(len(trndata))+'_instances/'
try:
    os.makedirs(args.modelname)
    print("Directory " , args.modelname ,  " Created ") 
except FileExistsError:
    print("Directory " , args.modelname ,  " already exists")
args.save_path = args.modelname +  str(args.epochs)+'epochs.pt'
args.log_path =  args.modelname +  str(args.epochs)+'epochs.log'
args.fig_path =  args.modelname +  str(args.epochs)+'epochs.png'
args.logger = Logger(args.log_path)
with open(args.modelname+'/surf_vocab.json', 'w') as f:
    f.write(json.dumps(vocab.word2id))
model_init = uniform_initializer(0.01)
emb_init = uniform_initializer(0.1)
args.ni = 512
args.enc_nh = 1024
args.enc_dropout_in = 0.0
args.enc_dropout_out = 0.0

args.model = CharLM(args, vocab, model_init, emb_init) 
args.model.to(args.device)  
args.logger.write('\nnumber of params: %d \n' % count_parameters(args.model))
args.logger.write(args)
args.logger.write('\n')
train(batches, args)
breakpoint()
plt.savefig(args.fig_path)
