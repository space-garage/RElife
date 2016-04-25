/*
 * onewire.c
 *
 *  Created on: 13.02.2012
 *      Author: di
 */
#include "cmsis_os.h"
#include "onewire.h"
#include "stm32f1xx_hal.h"

UART_HandleTypeDef huart;
HAL_StatusTypeDef ret;
// Буфер для приема/передачи по 1-wire
uint8_t ow_buf[8];

#define OW_0	0x00
#define OW_1	0xff
#define OW_R_1	0xff

//-----------------------------------------------------------------------------
// функция преобразует один байт в восемь, для передачи через UART
// ow_byte - байт, который надо преобразовать
// ow_bits - ссылка на буфер, размером не менее 8 байт
//-----------------------------------------------------------------------------
void OW_toBits(uint8_t ow_byte, uint8_t *ow_bits) {
	uint8_t i;
	for (i = 0; i < 8; i++) {
		if (ow_byte & 0x01) {
			*ow_bits = OW_1;
		} else {
			*ow_bits = OW_0;
		}
		ow_bits++;
		ow_byte = ow_byte >> 1;
	}
}

//-----------------------------------------------------------------------------
// обратное преобразование - из того, что получено через UART опять собирается байт
// ow_bits - ссылка на буфер, размером не менее 8 байт
//-----------------------------------------------------------------------------
uint8_t OW_toByte(uint8_t *ow_bits) {
	uint8_t ow_byte, i;
	ow_byte = 0;
	for (i = 0; i < 8; i++) {
		ow_byte = ow_byte >> 1;
		if (*ow_bits == OW_R_1) {
			ow_byte |= 0x80;
		}
		ow_bits++;
	}

	return ow_byte;
}

//-----------------------------------------------------------------------------
// инициализирует UART и DMA
//-----------------------------------------------------------------------------

void MX_UART_UART_Init(int spd)
{
  huart.Instance = USART3;
  huart.Init.BaudRate = spd;
  huart.Init.WordLength = UART_WORDLENGTH_8B;
  huart.Init.StopBits = UART_STOPBITS_1;
  huart.Init.Parity = UART_PARITY_NONE;
  huart.Init.Mode = UART_MODE_TX_RX;
  huart.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart.Init.OverSampling = UART_OVERSAMPLING_16;
  HAL_HalfDuplex_Init(&huart);
}
uint8_t OW_Init() {

  MX_UART_UART_Init(115200);
  return OW_OK;
}
//-----------------------------------------------------------------------------
// осуществляет сброс и проверку на наличие устройств на шине
//-----------------------------------------------------------------------------
int glob_evel=0;

/*
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    glob_evel=1;
}
*/

uint8_t OW_Reset() {
	uint8_t ow_presence;

    MX_UART_UART_Init(9600);
	// отправляем 0xf0 на скорости 9600 __HAL_UART_CLEAR_FLAG
	//__HAL_UART_CLEAR_FLAG(huart, UART_FLAG_TC)
	//UART_ClearFlag(OW_UART, UART_FLAG_TC);
	HAL_UART_Receive_DMA(&huart, ow_buf, 1); //HAL_StatusTypeDef  ret
	char a=0xf0 ;
	HAL_UART_Transmit_DMA(&huart, &a, 1); //HAL_StatusTypeDef  ret
	//UART_SendData(OW_UART, 0xf0);
	while (!glob_evel); glob_evel=0;
	//while (UART_GetFlagStatus(OW_UART, UART_FLAG_TC) == RESET) {
//#ifdef OW_GIVE_TICK_RTOS
		//taskYIELD();
//#endif
	//}

	ow_presence = ow_buf[0];
    MX_UART_UART_Init(115200);

	if (ow_presence != 0xf0) {
		return OW_OK;
	}

	return OW_NO_DEVICE;
}


//-----------------------------------------------------------------------------
// процедура общения с шиной 1-wire
// sendReset - посылать RESET в начале общения.
// 		OW_SEND_RESET или OW_NO_RESET
// command - массив байт, отсылаемых в шину. Если нужно чтение - отправляем OW_READ_SLOTH
// cLen - длина буфера команд, столько байт отошлется в шину
// data - если требуется чтение, то ссылка на буфер для чтения
// dLen - длина буфера для чтения. Прочитается не более этой длины
// readStart - с какого символа передачи начинать чтение (нумеруются с 0)
//		можно указать OW_NO_READ, тогда можно не задавать data и dLen
//-----------------------------------------------------------------------------
uint8_t OW_Send(uint8_t sendReset, uint8_t *command, uint8_t cLen,
		uint8_t *data, uint8_t dLen, uint8_t readStart) {



	// если требуется сброс - сбрасываем и проверяем на наличие устройств
	if (sendReset == OW_SEND_RESET) {
		if (OW_Reset() == OW_NO_DEVICE) {
			return OW_NO_DEVICE;
		}
	}

	while (cLen > 0) {

		OW_toBits(*command, ow_buf);
		command++;
		cLen--;

/*

		// Ждем, пока не примем 8 байт

		while (DMA_GetFlagStatus(OW_DMA_FLAG) == RESET){
#ifdef OW_GIVE_TICK_RTOS
			taskYIELD();
#endif
		}

        */

        ret = HAL_UART_Receive_DMA(&huart, ow_buf, 8); //HAL_StatusTypeDef  ret

        ret = HAL_UART_Transmit_DMA(&huart, ow_buf, 8); //HAL_StatusTypeDef  ret
        //HAL_Delay(100);
        while (!glob_evel);
        glob_evel=0;
        ret = HAL_UART_DMAStop(&huart);

		// если прочитанные данные кому-то нужны - выкинем их в буфер
		if (readStart == 0 && dLen > 0) {
			*data = OW_toByte(ow_buf);
			data++;
			dLen--;
		} else {
			if (readStart != OW_NO_READ) {
				readStart--;
			}
		}
	}

	return OW_OK;
}

