'''
TAF Programme designed to return a graphical interpretation

@TODO: Graphical Output
       Create Class for each change group
'''
import datetime as dt
EXAMPLE = '''EGXE 161400Z 1615/1702 22015KT 9999 FEW020 SCT025 TEMPO 1622/1702 24022G32KT SCT020 BECMG 1615/1619 5000 -RA 30010KT'''
SPLITS = ['BECMG', 'TEMPO', 'PROB40', 'PROB30']
ALLOWED_WX = ['-RA']
CLOUD_AMTS = ['FEW','SCT','BKN','OVC']

TABLE = "<table border=2>"
TABLE_ = "</table>"
TR = "\n<tr>"
TR_ = "</tr>"
TD = "<td>"
TD_ = "</td>"


class Taf():

    def __init__(self, raw):
        self.raw = raw
        self.groups_raw = self.get_taf_as_dict()
        self.groups_proc = self.process_groups()

    def __str__(self):
        a = self.groups_raw
        b = self.groups_proc        
        msg = "\nGroups raw is:\n{}\nGroups proc is:\n".format(a)
        for key, item in b.iteritems():
            msg = msg + str(key) + " : " + str(item) + "\n\n"
        return msg


    def html_out(self):
        """
        Creates an html table with output
        @todo tidy up - 
            work out how.format works and 
            put all inputs in tidy lists
        """
        out = "<br>{}<br>".format(self.groups_proc['ICAO'])
        out = out + TABLE + TR
        out = out + "<td colspan={}>{}</td>".format(self.groups_proc['total_duration'],
                                                    " ".join(self.groups_raw[0]))
        out = out + TR_ + TR
        i = 0
        while i < self.groups_proc['total_duration']:
            start =(int(self.groups_proc['base_time']))
            out = out + TD + str(start + i) + TD_
            i += 1
        out = out + TR + self.groups_proc['base_group']['vis_colour']['colour'] + TR_
        for key, item in self.groups_proc.iteritems():
            out = out + TR
            if isinstance(key, int):
                # group_type
                # <td colspan = {}>
                if item['time_start_since_ref'] == 0:
                    out = out + "<td colspan={}>{}</td>".format(item['duration'],
                                                            item['change_type'])
                    out = out + TR_ + TR
                    # vis     
                    out = out + "<td colspan={} bgcolor={}>{} - {}</td>".format(item['duration'],
                                                                item['vis_colour']['hex'],
                                                                item['vis_colour']['colour'],
                                                                item['vis'])
                    out = out + TR_ + TR
                    # cloud   
                    out = out + "<td colspan={} bgcolor={}>{} - {}</td>".format(item['duration'], item['clouds']['colour']['hex'], item['clouds']['colour']['colour'], item['clouds']['lowest_base'])
                    out = out + TR_ + TR
                    # wind
                    out = out + "<td colspan={}>{}</td>".format(item['duration'], item['wind'])
                else:            
                    out = out + "<td colspan={}></td>".format(item['time_start_since_ref'])
                    out = out + "<td colspan={}>{}</td>".format(item['duration'],
                                                            item['change_type'])
                    out = out + TR_ + TR
                    # vis                
                    out = out + "<td colspan={}></td>".format(item['time_start_since_ref'])
                    out = out + "<td colspan={} bgcolor={}>{} - {}</td>".format(item['duration'],
item['vis_colour']['hex'],
                                                                item['vis_colour']['colour'],
                                                                item['vis'])
                    out = out + TR_ + TR
                    # cloud                
                    out = out + "<td colspan={}></td>".format(item['time_start_since_ref'])
                    out = out + "<td colspan={} bgcolor={}>{} - {} FT</td>".format(item['duration'], item['clouds']['colour']['hex'] ,item['clouds']['colour']['colour'], item['clouds']['lowest_base'])
                    out = out + TR_ + TR
                    # wind               
                    out = out + "<td colspan={}></td>".format(item['time_start_since_ref'])
                    out = out + "<td colspan={}>{}</td>".format(item['duration'], item['wind'])


            else:
                pass
            out = out + TR_
        out = out + TABLE_
        return(out)


    # def html_tr(self)   


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
        out = {'groups':[]}
        
        for cloud in clouds:            
            detail = {'height': int(cloud[3:]) * 100, 'amt': cloud[:3]}
            out['groups'].append(detail)
                
        lowest_base = 10000
        for cloud in out['groups']:
            if cloud['height'] < lowest_base and cloud['amt'] in sig_cloud:
                lowest_base = cloud['height']
        out['lowest_base'] = lowest_base
        if lowest_base >= 2500:
            out['colour'] = {'colour':'BLU', 'hex':'#0000EE'}        
        elif lowest_base < 2500:
            out['colour'] = {'colour':'WHT', 'hex': '#EEEEEE'}
        elif lowest_base < 1500:
            out['colour'] = {'colour':'GRN', 'hex': '#00EE00'}
        elif lowest_base < 700:
            out['colour'] = {'colour':'YL01', 'hex': '#00EEEE'}
        elif lowest_base < 500:
            out['colour'] = {'colour':'YLO2', 'hex': '#00AAAA'}
        elif lowest_base < 300:
            out['colour'] = {'colour':'AMB', 'hex': '#CC8888'}
        elif lowest_base < 200:
            out['colour'] = {'colour':'RED', 'hex': '#EE0000'}
        else:
            out['colour'] = {'colour':'NIL', 'hex': '#000000'}
        return out


    def taf_duration(self, timegr):
        '''
        Takes a DDHH/DDHH timegroup and
        returns a length in hours
        @todo: Make fail sensibly
        '''
        start, end = timegr.split('/')
        times2 = []
        for time in [start, end]:
            time = self.guess_year_month() + time
            times2.append(dt.datetime.strptime(time, "%Y%m%d%H"))
        return((times2[1] - times2[0]).seconds // 3600)


    def cloud_analysis(self, clouds):
        '''
        takes a list of clouds in string form and returns dicts
        '''
        if len(clouds) == 0:
            return {'colour': {'colour': '', 'hex': ''}, 'lowest_base':'no lowest sig base'}
        else:
            clouds = self.get_cloud_group_dict(clouds)
            return clouds


    def vis_colour(self, vis):
        '''
        Takes a raw vis and returns a vis colour dictionary including
        both colour state and a hex code for plotting that colour
        '''
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



    def guess_year_month(self):
        '''
        guesses the appropriate year and month
        @TODO - implement this!
        '''
        return "201703"


    def dict_tafgroup(self, tafgroup):
        '''
        takes taf data and turns it into a dict.
        '''
        out = {'clouds': [], 'wx': [], 'duration': 0, 'vis':None, 'vis_colour':{'colour': 'NIL', 'hex': '#00000000'}}
        clouds = []
        for word in tafgroup:
            # this will break if vv/// is in forecast :(
            if '/' in word:
                out['time_group'] = word
                times = word.split('/')
                times.append(self.groups_raw['base_time'])
                times2 = []
                for time in times:
                    time = self.guess_year_month() + time
                    times2.append(dt.datetime.strptime(time, "%Y%m%d%H"))
                out['time_start'] = times2[0]
                out['time_end'] = times2[1]
                out['time_start_since_ref'] = (times2[0] - times2[2]).seconds // 3600
                out['duration'] = (times2[1] - times2[0]).seconds // 3600
            elif word in SPLITS:
                out['change_type'] = word
            elif len(word) == 4:
                out['vis'] = int(word)
                out['vis_colour'] = self.vis_colour(int(word))
            elif word[-2:] == "KT":
                out['wind'] = word
                out['max_wind'] = word[-4:-2]
            elif word[:3] in CLOUD_AMTS:
                clouds.append(word)
            elif word in ALLOWED_WX:
                out['wx'].append(word)
        out['clouds'] = self.cloud_analysis(clouds)
        

        return out

    def process_group(self):
        out = {}
        # out = {'clouds': [], 'wx': [], 'duration': 0, 'vis':None, 'vis_colour':{'colour': 'NIL', 'hex': '#00000000'}}        
        for label, tafgroup in self.groups_raw.iteritems():
            if label == 'base_time':
                out['base_time'] = tafgroup
            elif label == 0:
                out['ICAO'] = tafgroup[0]
                out['total_duration'] = self.taf_duration(tafgroup[2])
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
    print Taf(EXAMPLE).html_out()


    
                     
        
if __name__ == "__main__":
    main()
