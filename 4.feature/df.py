import operator

# Document Frequency

class DF:
    def generate_merged_dict_by_df(self, doc_list):
        df_dict = dict()
        for tmp in doc_list:
            doc = tmp[list(tmp.keys())[0]]
            for keyword in doc.keys():
                if keyword in df_dict.keys():
                    df_dict[keyword] += 1
                else:
                    df_dict[keyword] = 1

        return df_dict

    def generate_merged_dict_by_ttf(self, doc_list):
        ttf_dict = dict()
        for tmp in doc_list:
            doc = tmp[list(tmp.keys())[0]]
            for keyword in doc.keys():
                if keyword in ttf_dict.keys():
                    ttf_dict[keyword] += doc[keyword]
                else:
                    ttf_dict[keyword] = doc[keyword]

        return ttf_dict