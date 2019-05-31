import torch
import torch.nn as nn
import torch.nn.functional as F

class ubdlMPID( nn.Module ):

    def __init__(self, img_width, img_height, num_class=5, keep_prob=0.5,
                 base_filters=64, add_filters=32,
                 num_blocks=5, layers_in_block=2, weight_file=None):
        nn.Module.__init__(self)

        self.num_blocks      = num_blocks
        self.layers_in_block = layers_in_block
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
                                  padding=1, bias=True )
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
        print "predicted linear_features=",in_features," width=",width," height=",height
        
        self.fc = nn.Linear( in_features, num_class )
        
        if weight_file is None:
            pass
        else:
            pass
                                  

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

    def show_sizes(self,mode=True):
        self.show_sizes = mode

if __name__ == "__main__":

    img = torch.zeros( (5,1,512,512), dtype=torch.float ).to( "cpu" )

    print img.shape, img.is_cuda


    model = ubdlMPID( 512, 512 )
    print model

    out = model(img)
