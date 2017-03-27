'''
TAF Programme designed to return a graphical interpretation

@TODO: Graphical Output
       Create Class for each change group
'''

EXAMPLE = '''EGXE 161400Z 1615/1702 22015KT 9999 FEW020 SCT025 TEMPO 1622/1702 24022G32KT SCT020 BECMG 1615/1619 5000 -RA 30010KT'''
SPLITS = ['BECMG', 'TEMPO', 'PROB40', 'PROB30']
ALLOWED_WX = ['-RA']


class Taf():

    def __init__(self, raw):
        self.raw = raw
        self.groups_raw = self.get_taf_as_dict()

    def __str__(self):
        return str(self.groups_raw)

    def get_taf_as_dict(self):
        '''
        Function to return a dictionary each item of which is a change group
        item 0 will always be the base conditions
        item zero in each key will always be the change group
        '''
        taf = self.raw.split(' ')
        taf_dict_key = 0
        taf_dict = {0: []}
        for word_from_taf in taf:
            if word_from_taf in SPLITS:
                taf_dict_key = taf_dict_key + 1
                taf_dict[taf_dict_key] = [word_from_taf]
            else:
                taf_dict[taf_dict_key] = taf_dict[taf_dict_key] + [word_from_taf]
        taf_dict['base_time'] = taf_dict[0][2][:4]
        return taf_dict


    def taf_datetime_difference(a, b):
        '''
        calculates a difference in hours between two taf
        datetimes
        '''
        import datetime as dt
        dt.datetime.strptime(a, '%D')




def main():
    '''
    blah
    '''
    print Taf(EXAMPLE)

    
                     
    
if __name__ == "__main__":
    main()
