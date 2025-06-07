#include "i2c_lcd.h"
#include "main.h"

extern I2C_HandleTypeDef hi2c1;

void i2c_lcd_init(void)
{
	HAL_Delay(50);
	lcd_command(0x33); lcd_command(0x32);
	lcd_command(LCD_FUNC); lcd_command(LCD_ON);
	lcd_command(LCD_ENTRY); lcd_command(LCD_CLEAR);
	HAL_Delay(2);
}

void lcd_command(uint8_t cmd)
{
	uint8_t h=cmd&0xF0, l=(cmd<<4)&0xF0;
	uint8_t d[4]={h|0x04|BACKLIGHT,h|BACKLIGHT,l|0x04|BACKLIGHT,l|BACKLIGHT};
	HAL_I2C_Master_Transmit(&hi2c1, I2C_LCD_ADDR, d, 4, 100);
}

void lcd_data(uint8_t data_byte)
{
	uint8_t h=data_byte&0xF0,l=(data_byte<<4)&0xF0;
	uint8_t d[4]={h|0x05|BACKLIGHT,h|0x01|BACKLIGHT,l|0x05|BACKLIGHT,l|0x01|BACKLIGHT};
	HAL_I2C_Master_Transmit(&hi2c1, I2C_LCD_ADDR, d, 4, 100);
}

void lcd_string(uint8_t *str){while(*str) lcd_data(*str++);}
void move_cursor(uint8_t row,uint8_t col){lcd_command(0x80|(row<<6)|col);}
