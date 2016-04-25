#ifndef GYROW_H_INCLUDED
#define GYROW_H_INCLUDED

#define PYB_I2C_MASTER_ADDRESS (0xfe)

typedef struct {
    int16_t ax;
    int16_t ay;
    int16_t az;
    int16_t gx;
    int16_t gy;
    int16_t gz;

}gyrValTypeDef;


void gyro_start(void);
void gyro_init(void);
uint32_t GetAccel(void);

#endif /* GYROW_H_INCLUDED */
