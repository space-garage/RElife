#include "stm32f1xx_hal.h"
#include "mpu6050.h"
#include "gyroW.h"
#include "math.h"
#include "arm_math.h"
#include "arm_common_tables.h"
I2C_HandleTypeDef I2CHandle1;

void gyro_start(void);
void gyro_init(void);
uint32_t GetAccel(void);

void gyro_start(void)
{

    // start the I2C bus in master mode
    I2CHandle1.Instance = I2C1;
    I2CHandle1.Init.AddressingMode  = I2C_ADDRESSINGMODE_7BIT;
    I2CHandle1.Init.ClockSpeed      = 400000;
    I2CHandle1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLED;
    I2CHandle1.Init.DutyCycle       = I2C_DUTYCYCLE_16_9;
    I2CHandle1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLED;
    I2CHandle1.Init.NoStretchMode   = I2C_NOSTRETCH_DISABLED;
    I2CHandle1.Init.OwnAddress1     = PYB_I2C_MASTER_ADDRESS;
    I2CHandle1.Init.OwnAddress2     = 0xfe; // unused

    HAL_I2C_DeInit(&I2CHandle1);
    HAL_I2C_Init(&I2CHandle1);

    HAL_StatusTypeDef status;

    //printf("IsDeviceReady\n");
    for(int i = 0; i < 10; i++)
    {
        status = HAL_I2C_IsDeviceReady(&I2CHandle1,
                                       MPU6050_ADDR,
                                       10,
                                       200);

        //printf("  got %d\n", status);
        if(status == HAL_OK)
        {
            break;
        }

    }
    if (status !=HAL_OK) while(1);

}

void gyro_init(void)
{

    // Call init
    mpu6050_init();
    HAL_Delay(50);


}

uint32_t GetAccel(void){
  gyrValTypeDef gVal;
  q31_t res;
  mpu6050_getRawData(&gVal.ax,&gVal.ay,&gVal.az,&gVal.gx,&gVal.gy,&gVal.gz);
  uint32_t x=gVal.ax*gVal.ax, y=gVal.ay*gVal.ay, z=gVal.az*gVal.az, s=x+y+z;
  /*
  if (ARM_MATH_SUCCESS== arm_sqrt_q31(s, &res)){
    return res;
  }
  else while(1);
  */

  res=(uint32_t)sqrtf((float)s);
  return res;
}
