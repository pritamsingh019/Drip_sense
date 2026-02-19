#ifndef AT_PARSER_H
#define AT_PARSER_H

typedef void (*at_handler_t)(const char *args);

void at_register(const char *command, at_handler_t handler);
void at_process_line(const char *line);

#endif // AT_PARSER_H
