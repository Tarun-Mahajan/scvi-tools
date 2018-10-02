from scvi.harmonization.utils_chenling import get_matrix_from_dir
from scvi.dataset.dataset import GeneExpressionDataset
from scipy.sparse import csr_matrix
import numpy as np


class Paul(GeneExpressionDataset):
    def __init__(self, save_path='../Paul/'):
        self.save_path = save_path
        count, labels, cell_type, gene_names = self.preprocess()
        super(Paul, self).__init__(
            *GeneExpressionDataset.get_attributes_from_matrix(
                count, labels=labels),
            gene_names=np.char.upper(gene_names), cell_types=cell_type)
    def preprocess(self):
        count, geneid, cellid = get_matrix_from_dir(self.save_path.split('/')[1])
        label = np.genfromtxt(self.save_path + 'clusterid.tsv', dtype='int')
        # count, geneid, cellid = get_matrix_from_dir('Paul')
        # label = np.genfromtxt('../Paul/clusterid.tsv', dtype='int')
        count = csr_matrix(count.T)
        celltypes = np.asarray(['Ery6', #1
                                         'Ery5', #2
                                         'Ery4', #3
                                         'Ery3', #4
                                         'Ery2', #5
                                         'Ery1', #6
                                         'PreEry', #7
                                         'MegaK', #8
                                         'PreNeu', #9
                                         'PreMono', #10
                                         'DC', #11
                                         'Baso1', #12
                                         'Baso2', #13
                                         'Mono1', #14
                                         'Mono2', #15
                                         'Neu1', #16
                                         'Neu2', #17
                                         'Eos', #18
                                         'C19'
                                         ])
        return count, label,celltypes, geneid


class Tusi(GeneExpressionDataset):
    def __init__(self, save_path='../Tusi/'):
        self.save_path = save_path
        count, labels, cell_type, gene_names, time, batchid = self.preprocess()
        super(Tusi, self).__init__(
            *GeneExpressionDataset.get_attributes_from_matrix(
                count, labels=labels),
            gene_names=np.char.upper(gene_names), cell_types=cell_type)
        self.batch_indices = batchid.reshape(len(batchid), 1)
        self.time_traj = time

    def preprocess(self):
        count = np.genfromtxt(self.save_path+'raw.umi.csv',delimiter=',')
        meta = np.genfromtxt(self.save_path+'raw.meta.txt',delimiter=',',dtype='str')
        seq_run, batchid = np.unique(meta[meta[:,4]=='1',3],return_inverse=True)
        time = np.load(self.save_path+'bBM/V.npy')
        celltypes = np.genfromtxt(self.save_path+'bBM/fate_labels.csv',delimiter=',',dtype='str')
        labels = np.load(self.save_path+'bBM/B.npy')
        geneid = np.genfromtxt(self.save_path+'genes.csv',dtype='str',delimiter=',')
        labels = np.asarray([np.argmax(x) for x in labels])
        count = count[meta[1:,4]=='1',]
        count = count.astype('int')
        return count, labels, celltypes, geneid, time, batchid
