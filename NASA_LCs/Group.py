# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:09:29 2021

@author: jlbus
"""
import pandas as pd
import numpy as np

import os

import NASA_LCs.group_tools as gt
import NASA_LCs.catalog_queries as catQ

class Group:
    def __init__(self,name,group_df):
        self.name = str(name)
        self.group_df = group_df
        
    def add_tics(self,ra_col_name = 'ra',dec_col_name = 'dec', tic_col_name = None):
        if tic_col_name is not None:
            self.tics = self.group_df[tic_col_name].to_numpy(dtype = 'str')
        else:
            self.tics = catQ.get_tic_bulk(query_df = self.group_df,
                                          ra_col_name = ra_col_name, dec_col_name = dec_col_name)
            
    def add_TIC_info(self, ra_col_name = 'ra', dec_col_name = 'dec'):
        self.tics,self.TIC_query = catQ.get_TIC_data_bulk(query_df = self.group_df,
                                                          ra_col_name = ra_col_name, 
                                                          dec_col_name = dec_col_name)
    
    def add_gaia_info(self, ra_col_name = 'ra', dec_col_name = 'dec', gaia_kwrgs = 'all', id_col_name = None):
        self.gaia_query = catQ.get_gaia_data_bulk(query_df = self.group_df,
                                                 ra_col_name = ra_col_name, dec_col_name = dec_col_name,
                                                 gaia_kwrgs = gaia_kwrgs, id_col_name = id_col_name)        
    
    def add_tess_LCs(self,download_dir = None, lc_types = ['spoc','cpm']):
        ## need to expand to add spoc rots later
        tic_list = self.tics
        target_dict = gt.bulk_download(tic_list = tic_list, download_dir = download_dir, lc_types = ['cpm'])
        
        ## below could be used to update best_rots selection
        
        # if 'cpm' in lc_types:
        #     self.cpm_rot_container = {}
        #     for tic in target_dict.keys():
        #         target = target_dict[tic]
        #         if 'cpm_rot_dict' in target.available_attributes:
        #             self.cpm_rot_container[tic] = target.cpm_rot_dict
        #         else:
        #             self.cpm_rot_container[tic] = None
                    
        # if 'spoc' in lc_types:
        #     self.sap_rot_container = {}
        #     self.pdc_rot_contatiner = {}
        #     for tic in target_dict.keys():
        #         target = target_dict[tic]
        #         if 'sap_rot_dict' in target.available_attributes:
        #             self.sap_rot_container[tic] = target.sap_rot_dict
        #         else:
        #             self.sap_rot_container[tic] = None
        #         if 'pdc_rot_dict' in target.available_attributes:
        #             self.pdc_rot_container[tic] = target.pdc_rot_dict
        #         else:
        #             self.pdc_rot_container[tic] = None 
                    
        return(target_dict)
        
    def rot_summary(self,target_dict,lc_types = ['spoc','cpm']):
        self.best_rots_dict = gt.best_tess_rots(target_dict,lc_types)
        
    #def add_final_rots():
        #condition on rots_summary
    
    def add_pc_seq_fig(fig):#flux_type = 'cpm', color = 'bp_rp', final_rots_col = None,color_bar_kwrgs=None)
        self.pc_seq_fig = fig
    #     import matplotlib.pyplot as plt
        
    #     best_rots_df = self.best_rots_dict[flux_type]
    #     best_rots_merge = self.group_df.merge(right = best_rots_df, on = 'tic', how = 'left')
    #     best_rots_
    #     if final_rots_col is None:
    #         eff_temp = best_rots_merge[color]
    #         period = best_rots_merge['LS_Per1']
    
    #     fig = gt.pc_seq_fig(praesepe_on = False, hyades_on = False, upper_sco_on = True, xlim = (0.05,4.5))
        
    #     if final_rots_col is None:
    #         plt.scatter(best_rots_df['bp_rp'],best_rots_df['LS_Per1'], c = update_match_15['PROB'], cmap = "autumn", s = 80, alpha = 0.7, edgecolors = 'black')
    #     plt.title("Eps Cha - BANYAN Rotations")
    #     cbar = plt.colorbar()
    #     cbar.ax.get_yaxis().labelpad = 25
    #     cbar.ax.set_ylabel('BANYAN Probability', rotation=270)
    #     plot_fn = os.path.join(proj_fold,'eps_cha_banyan.png')