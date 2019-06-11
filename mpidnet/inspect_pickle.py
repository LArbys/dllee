import pickle

for plane in xrange(3):
    print "//////////////////////////////////"
    print "PLANE ",plane
    f = open('mpid_weights_plane%d.pickle'%(plane),'r')
    weights = pickle.load(f)

    for k,d in weights.items():
        print k,type(d),d.shape

    f.close()
