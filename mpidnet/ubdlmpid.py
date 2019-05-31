import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class ubdlMPID( nn.Module ):

    def __init__(self, img_width, img_height, num_class=5, keep_prob=0.5,
                 base_filters=64, add_filters=32, show_sizes=False,
                 num_blocks=5, layers_in_block=2, weight_file=None):
        nn.Module.__init__(self)

        self.num_blocks      = num_blocks
        self.layers_in_block = layers_in_block
        self.show_sizes = show_sizes
        outchs = base_filters
        inchs  = 1
        width  = int(img_width)
        height = int(img_height)
        for iblock in xrange(num_blocks):
            for ilayer in xrange(layers_in_block):

                stride = 1
                if iblock==0 and ilayer==0:
                    stride = 2
                    width  /= 2
                    height /= 2

                conv  = nn.Conv2d( inchs, outchs, 3, stride=stride,
                                  padding=1, bias=False )
                setattr( self, "conv%d_%d"%(iblock,ilayer), conv ) 
                setattr( self, "bn%d_%d"%(iblock,ilayer), nn.BatchNorm2d( outchs, track_running_stats=True ) )
                
                if iblock+1==num_blocks and ilayer+1==layers_in_block:
                    pass
                else:
                    setattr( self, "relu%d_%d"%(iblock,ilayer),  nn.ReLU() )

                inchs = outchs
                
            setattr( self, "pool%d"%(iblock), nn.AvgPool2d( 2 ) )
            if iblock+1<num_blocks:
                outchs += add_filters
            width /= 2
            height /= 2

        self.drop = nn.Dropout( p=keep_prob )

        in_features = outchs*width*height
        if self.show_sizes: print "predicted linear_features=",in_features," width=",width," height=",height
        
        self.fc = nn.Linear( in_features, num_class )
                                          

    def forward(self,x):
        
        for iblock in xrange(self.num_blocks):
            for ilayer in xrange(self.layers_in_block):

                # conv2d layer
                layer = getattr( self, "conv%d_%d"%(iblock,ilayer) )
                x = layer(x)

                if self.show_sizes:
                    print "conv%d_%d"%(iblock,ilayer)," ",x.shape," cuda=",x.is_cuda

                # batch norm
                # use functional if eval, use layer with running stats for training
                bn = getattr( self, "bn%d_%d"%(iblock,ilayer) )
                x = bn(x)

                if iblock+1==self.num_blocks and ilayer+1==self.layers_in_block:
                    pass
                else:
                    actfn = getattr(self, "relu%d_%d"%(iblock,ilayer))
                    x = actfn(x)
            # pooling
            pool = getattr(self,"pool%d"%(iblock))
            x = pool(x)
            if self.show_sizes:
                print "pool%d"%(iblock),": ",x.shape," cuda=",x.is_cuda
        
        # unroll
        x = x.view( x.size(0), -1 )

        if self.show_sizes:
            print "unrolled: ",x.shape," cuda=",x.is_cuda
        
        # dropout
        x = self.drop(x)

        # fully connected
        x = self.fc(x)

        if self.show_sizes:
            print "fc: ",x.shape," cuda=",x.is_cuda        

        return x

    def showSizes(self,mode=True):
        self.show_sizes = mode

    def load_from_pickle(self,pickle_filepath,debug=False):
        """
        load parameter values from pickle
        """
        import pickle
        
        # load pickle
        f = open(pickle_filepath,'r')
        weights = pickle.load(f)

        # set conv layers
        for iblock in xrange(self.num_blocks):
            for ilayer in xrange(self.layers_in_block):
                name="conv%d_%d"%(iblock,ilayer)
                conv = getattr(self,name)
                if debug: print name,": ",conv.weight.shape,type(conv.weight.data)

                storename = "toy_pid/conv%d_%d/weights:0"%(iblock,ilayer)
                arr = weights[storename]
                if debug: print storename,arr.shape,type(arr)
                if arr.shape[-1]!=conv.weight.shape[0]:
                    raise ValueError("mismatched shape")

                outch = arr.shape[-1]
                inch  = arr.shape[-2]

                # change to torch shape
                arr = np.transpose( arr, (3,2,0,1) )
                transpose = True
                
                if conv.weight.is_cuda:
                    arr_t = torch.from_numpy( arr ).to( conv.weight.data.get_device() )
                else:
                    arr_t = torch.from_numpy( arr ).to("cpu")


                if not transpose:
                    for och in xrange(outch):
                        for ich in xrange(inch):
                            conv.weight.data[och,ich,:,:] = arr_t[:,:,ich,och]
                else:
                    conv.weight.data[:] = arr_t[:]

        # set batch-norm layers
        for iblock in xrange(self.num_blocks):
            for ilayer in xrange(self.layers_in_block):
                name="bn%d_%d"%(iblock,ilayer)
                bn = getattr(self,name)
                if debug: print name,": gamma ",bn.weight.shape,type(bn.weight.data)
                if debug: print name,": beta ",bn.bias.shape,type(bn.bias.data)
                if debug: print name,": running_mean",bn.running_mean.shape,type(bn.running_mean)
                if debug: print name,": running_var",bn.running_var.shape,type(bn.running_var)

                par_v = {"beta":bn.bias.data,
                         "gamma":bn.weight.data,
                         "moving_mean":bn.running_mean,
                         "moving_variance":bn.running_var}
                
                arr_v = {}
                for varname in ["beta","moving_mean","moving_variance"]:# missing gamma
                    storename = "toy_pid/conv%d_%d/BatchNorm/%s:0"%(iblock,ilayer,varname)
                    arr = weights[storename]
                    if debug: print storename,arr.shape,type(arr)
                    if bn.weight.data.is_cuda:
                        arr_t = torch.from_numpy( arr ).to( bn.weight.data.get_device() )
                    else:
                        arr_t = torch.from_numpy( arr ).to( "cpu" )
                    par_v[varname][:] = arr_t[:]

                # gamma: set for one
                if bn.weight.data.is_cuda:
                    bn.weight.data[:] = torch.ones( bn.weight.shape ).to( bn.weight.data.get_device() )[:]
                else:
                    bn.weight.data[:] = torch.ones( bn.weight.shape )
                    
        # set FC layer
        fc_name="fc"
        fc_conv = getattr(self,fc_name)
        
        fc_wname = "toy_pid/fc0/weights:0"
        arr_w = weights[fc_wname]
        if debug: print fc_wname,arr_w.shape,type(arr_w)
        fc_bname = "toy_pid/fc0/biases:0"
        arr_b = weights[fc_bname]
        if debug: print fc_bname,arr_b.shape,type(arr_b)

        # change to torch shape
        arr_w = np.transpose( arr_w, (1,0) )
                
        if fc_conv.weight.is_cuda:
            arr_wt = torch.from_numpy( arr_w ).to( fc_conv.weight.data.get_device() )
            arr_bt = torch.from_numpy( arr_b ).to( fc_conv.bias.data.get_device() )            
        else:
            arr_wt = torch.from_numpy( arr_w ).to("cpu")
            arr_bt = torch.from_numpy( arr_b ).to("cpu")

        fc_conv.weight.data[:] = arr_wt[:]
        fc_conv.bias.data[:]   = arr_bt[:]


        


if __name__ == "__main__":

    img = torch.zeros( (5,1,512,512), dtype=torch.float ).to( "cpu" )

    print img.shape, img.is_cuda

    model = ubdlMPID( 512, 512 ).to("cuda")

    if True:
        print model

    if True:
        model.load_from_pickle('mpid_weights_plane2.pickle')
        
    if False:
        p = model.named_parameters()
        for k,v in p:        
            print k,type(v.data),v.data.shape," cuda=",v.data.is_cuda

            
    
    #model.showSizes()    
    #out = model(img)

