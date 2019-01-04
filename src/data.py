from quilt.data.elijahc import ripc

q_hash = lambda dnode: vars[dnode]['_hashes'][0]
  
class qloader():
    def _get_subjects(self):
        return self.nodes['subjects']()
    
    def _get_samples(self):
        return self.nodes['samples']()   
        
    def _get_targ_abs_quant(self):
        return self.nodes['targ_abs_quant']()
    
    def _get_targ_plasma_log2fc(self,form='long'):
        raw_df = self.nodes['targ_plasma_log2fc']()
        
        if form is 'long':
            return pd.melt(raw_df,id_vars=['sample_id','Subject','min'],value_name='log2fc',var_name='Name')
        else:
            return raw_df
    
    def __init__(self):
        # Identify each dataset by its hash
        self.nodes = {
            'subjects': ripc.meta.subjects,
            'samples': ripc.meta.samples,
        #     ripc.meta.metabolites,
            'targ_plasma_log2fc': ripc.targeted.plasma_log2fc,
            'targ_abs_quant': ripc.targeted.abs_quant
        }
        
        self.hash_map = {q_hash(v):k for k,v in nodes.items()}
        self.func_map = { qhash:getattr(self,'_get_'+v) for qhash,v in self.hash_map.items()}
        
    def get(self,dnode,**kwargs):
        qh = q_hash(dnode)
        raw_df = dnode()
        process = getattr(self,'_'+self.hash_map[qh])
        
        return process(raw_df,**kwargs)