
    def gen_frame(self):
        df = pd.DataFrame.from_dict(self.lbdict, orient='index')
        df.index = df.index.values.astype(int)
        df = df.sort_index()
        df['label'] = df.index.values.astype(int)
        df = df.reset_index(drop=True)
        return df
    
    def gen_multiframe(self):
        df = pd.DataFrame.from_dict(self.lbdict, orient='index')
        df.index = df.index.values.astype(int)
        df = df.sort_index()
        df['label'] = df.index.values.astype(int)
        df = df.reset_index(drop=True)
        df = df.apply(
                pd.Series.explode
                ).reset_index().set_index('index')
        df = df.set_index(df.groupby(['index']).cumcount(),
                append=True)
        return df

    def print_dict(self):
        json.dumps(self.get_dict())
        return

    def get_dict(self):
    #    return self.lbdict 
        pass
    def get_frame(self):
        #return self.frame()
        pass 

