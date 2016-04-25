#ifndef SIGNAL_MANAGEMENT_H_INCLUDED
#define SIGNAL_MANAGEMENT_H_INCLUDED

#define green_zone 3400
#define init_pwm_seek_step 500
#define pwm_seek_step_div 5
#define sigMnPer (500) //signal management period each 1/100 sec.

#include "stm32f1xx_hal.h"

typedef enum {under,in,over} adc_pos;

typedef struct {
    uint16_t adc_val;
    uint16_t pwm;
    uint16_t green_zone_l;
    uint16_t green_zone_h;
    uint16_t PwmSkSt; //pwm_seek_step
    adc_pos past_pos;



}SgMnStTypeDef;


int pwmProc (SgMnStTypeDef* );
int sigMnChk(SgMnStTypeDef* );

#endif /* SIGNAL_MANAGEMENT_H_INCLUDED */
