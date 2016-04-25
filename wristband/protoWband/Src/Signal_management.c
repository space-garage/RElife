#include "Signal_management.h"

int sigMnChk(SgMnStTypeDef* ps){


    if (ps->past_pos!=in) return 1;
    else{
        if (ps->adc_val > ps->green_zone_h){
            ps->past_pos=over;
            ps->PwmSkSt=init_pwm_seek_step;
            return 1;
        }

        if (ps->adc_val < ps->green_zone_l){
            ps->past_pos=under;
            ps->PwmSkSt=init_pwm_seek_step;
            return 1;
        }

        //ps->PwmSkSt=init_pwm_seek_step;

        return 0;
    }
}



int pwmProc (SgMnStTypeDef* ps){
    if (ps->adc_val>ps -> green_zone_h){
        if (ps->past_pos==under){
            ps->past_pos=over;
            ps->PwmSkSt/=pwm_seek_step_div;
        }

        ps->pwm += ps->PwmSkSt;
        return 1;
    }



    if (ps->adc_val<ps -> green_zone_l){
        if (ps->past_pos==over){
            ps->past_pos=under;
            ps->PwmSkSt/=pwm_seek_step_div;
        }

        if(0<(ps->pwm-ps->PwmSkSt)) ps->pwm-=ps->PwmSkSt;
        else ps->pwm = 0;
        return 1;

    }

    ps->past_pos=in;
    return 0;


}
