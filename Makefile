##
## EPITECH PROJECT, 2019
## Makefile
## File description:
## Gomoku
##

all:
	cp pbrain-protocol.py pbrain-gomoku-ai
	chmod +x pbrain-gomoku-ai

clean:

fclean:	clean
	-rm pbrain-gomoku-ai

re:	fclean all

.PHONY:	all clean fclean re
