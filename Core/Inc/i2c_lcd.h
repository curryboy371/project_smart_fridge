#ifndef I2C_LCD_H_
#define I2C_LCD_H_

#include <stdint.h>

#define I2C_LCD_ADDR (0x27<<1)
#define BACKLIGHT 0x08
#define LCD_CLEAR 0x01
#define LCD_HOME  0x02
#define LCD_ON    0x0C
#define LCD_FUNC  0x28
#define LCD_ENTRY 0x06

void i2c_lcd_init(void);
void lcd_command(uint8_t cmd);
void lcd_data(uint8_t data_byte);
void lcd_string(uint8_t *str);
void move_cursor(uint8_t row, uint8_t col);

#endif /* I2C_LCD_H_ */
