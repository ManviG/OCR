from __future__ import division
__author__ = 'blumonkey'


flist=["res3_acl2_out.txt"]
for fname in flist:
    fp=0
    tn=0
    tp=0
    with open(fname, "r") as ins:
        for line in ins:
            tags = line.split('\t')
            if(len(tags)>1):
                tags[-1]=tags[-1].strip('\n')
                if tags[-1]==tags[-2]=="1":
                    print(tags[0]+" "+tags[1]+"***")
                    tp=tp+1
                if tags[-1]=="1" and tags[-2]=="0":
                    print(tags[0]+" "+tags[1]+"+++")
                    fp=fp+1
                if tags[-1]=="0" and tags[-2]=="1":
                    print(tags[0]+" "+tags[1]+"---")
                    tn=tn+1
        print "TP:%d\tTN:%d\tFP:%d" % (tp,tn,fp)
    precision = tp/(tp+fp)
    recall = tp/(tp+tn)
    fscore = (2*precision*recall)/(precision+recall)
    print "Precision: ",precision
    print "Recall: ",recall
    print "f-score: ",fscore