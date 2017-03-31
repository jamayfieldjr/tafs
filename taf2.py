'''
TAF Programme designed to return a graphical interpretation

@TODO: Graphical Output
       Create Class for each change group
'''
import datetime as dt
EXAMPLE = '''EGXE 161400Z 1615/1702 22015KT 9999 FEW020 SCT025 TEMPO 1622/1702 24022G32KT SCT020 BECMG 1615/1619 5000 -RA 30010KT'''
SPLITS = ['BECMG', 'TEMPO', 'PROB40', 'PROB30']
ALLOWED_WX = ['-RA']


class Taf():

    def __init__(self, raw):
        self.raw = raw
        self.groups_raw = self.get_taf_as_dict()
        self.groups_proc = self.process_groups()

    def __str__(self):
        a = self.groups_raw
        b = self.groups_proc        
        msg = "\nGroups raw is:\n{}\nGroups proc is:\n{}".format(a,b)
        return msg

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

    def process_groups(self):
        for label, group in self.groups_raw.iteritems():
            if label == 'base_time':
                pass
            else:
                out = self.process_group()
            return out


    def get_cloud_group_dict(self, clouds, mil_rules=True):
        '''
        Returns a list of dictionaries, one for each cloud
        group and one for the lowest cloud height
        '''
        if mil_rules is True:
            sig_cloud = ['SCT', 'BKN', 'OVC']
        elif mil_rules is False:
            sig_cloud = ['BKN', 'OVC']
        out = []
        for cloud in clouds:
            detail = {'height': int(cloud[3:]) * 100, 'amt': cloud[:3]}
            out.append(detail)
        lowest_base = 10000
        for cloud in out:
            if cloud['height'] < lowest_base and cloud['amt'] in sig_cloud:
                lowest_base = cloud['height']
        out.append({'lowest_base': lowest_base})
        return out

    def cloud_analysis(self, clouds):
        '''
        takes a list of clouds in string form and returns dicts
        '''
        if len(clouds) == 0:
            return ['nsc']
        else:
            clouds = self.get_cloud_group_dict(clouds)
            return clouds

    def vis_colour(self, vis):
        if vis > 7999:
            vis_colour = {'colour': 'BLU', 'hex':'#0000EE'}
        elif vis > 4999:
            vis_colour = {'colour': 'WHT', 'hex':'#EEEEEE'}
        elif vis > 3699:
            vis_colour = {'colour': 'GRN', 'hex':'#00EE00'}
        elif vis > 2499:
            vis_colour = {'colour': 'YLO1', 'hex':'#00EEEE'}
        elif vis > 1599:
            vis_colour = {'colour': 'YLO2', 'hex':'#00AAAA'}
        elif vis > 799:
            vis_colour = {'colour': 'AMB', 'hex':'#CC8888'}
        elif vis < 800:
            vis_colour = {'colour': 'RED', 'hex':'#EE0000'}
        else:
            vis_colour = {'colour': 'ERR', 'hex':'#000000'}
        return vis_colour


    def dict_tafgroup(self, tafgroup):
        '''
        takes taf data and turns it into a dict.
        '''
        out = {'clouds': [], 'wx': [], 'duration': 0, 'vis':None, 'vis_colour':{'colour': 'NIL', 'hex': '#00000000'}}
        clouds = []
        for word in tafgroup:
            if '/' in word:
                out['time_group'] = word
                out['hour_start'] = word.split('/')[0][2:]
                out['hour_end'] = word.split('/')[1][2:]
                out['day_start'] = word.split('/')[0][:2]
                out['day_end'] = word.split('/')[1][:2]
                end_time = 24 * int(out['day_end']) + int(out['hour_end'])
                start_time = 24 * int(out['day_start']) + int(out['hour_start'])
                out['duration'] = end_time - start_time
            elif word in SPLITS:
                out['change_type'] = word
            elif len(word) == 4 and isinstance(int(word), int):
                out['vis'] = int(word)
                out['vis_colour'] = self.vis_colour(int(word))
            elif word[-2:] == "KT":
                out['wind'] = word
                out['max_wind'] = word[-4:-2]
            elif len(word) == 6:
                clouds.append(word)
            elif word in ALLOWED_WX:
                out['wx'].append(word)
        out['clouds'] = self.cloud_analysis(clouds)
        out['start_time_since_base'] = "Dave"

        return out

    def process_group(self):
        out = {}
        # out = {'clouds': [], 'wx': [], 'duration': 0, 'vis':None, 'vis_colour':{'colour': 'NIL', 'hex': '#00000000'}}        
        for label, tafgroup in self.groups_raw.iteritems():
            if label == 'base_time':
                out['base_time'] = tafgroup
            elif label == 0:
                out['ICAO'] = tafgroup[0]
                out['base_group'] = self.dict_tafgroup(tafgroup[3:])
            else:
                out[label] = self.dict_tafgroup(tafgroup)
        return out


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
