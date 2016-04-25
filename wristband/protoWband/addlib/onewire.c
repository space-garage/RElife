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
// ����� ��� ������/�������� �� 1-wire
uint8_t ow_buf[8];

#define OW_0	0x00
#define OW_1	0xff
#define OW_R_1	0xff

//-----------------------------------------------------------------------------
// ������� ����������� ���� ���� � ������, ��� �������� ����� UART
// ow_byte - ����, ������� ���� �������������
// ow_bits - ������ �� �����, �������� �� ����� 8 ����
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
// �������� �������������� - �� ����, ��� �������� ����� UART ����� ���������� ����
// ow_bits - ������ �� �����, �������� �� ����� 8 ����
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
// �������������� UART � DMA
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
// ������������ ����� � �������� �� ������� ��������� �� ����
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
	// ���������� 0xf0 �� �������� 9600 __HAL_UART_CLEAR_FLAG
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
// ��������� ������� � ����� 1-wire
// sendReset - �������� RESET � ������ �������.
// 		OW_SEND_RESET ��� OW_NO_RESET
// command - ������ ����, ���������� � ����. ���� ����� ������ - ���������� OW_READ_SLOTH
// cLen - ����� ������ ������, ������� ���� ��������� � ����
// data - ���� ��������� ������, �� ������ �� ����� ��� ������
// dLen - ����� ������ ��� ������. ����������� �� ����� ���� �����
// readStart - � ������ ������� �������� �������� ������ (���������� � 0)
//		����� ������� OW_NO_READ, ����� ����� �� �������� data � dLen
//-----------------------------------------------------------------------------
uint8_t OW_Send(uint8_t sendReset, uint8_t *command, uint8_t cLen,
		uint8_t *data, uint8_t dLen, uint8_t readStart) {



	// ���� ��������� ����� - ���������� � ��������� �� ������� ���������
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

		// ����, ���� �� ������ 8 ����

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

		// ���� ����������� ������ ����-�� ����� - ������� �� � �����
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

