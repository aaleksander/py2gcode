# -*- coding: utf-8 -*-
from Tkinter import *
from math import cos, sin




# разбор строки path из SVG-файла


svg1 = "M 215.71429,600.93361 170,423.79075 380,369.50504 450,520.93361 z" #нарисовать четыре точки и замкнуть

trim :: String -> String
trim = f . f
   where f = reverse . dropWhile isSpace

splitPath :: String -> [String]
splitPath [] = []
splitPath (x:xs) 	
	| [] <- xs = [[x]] --нужно, чтобы из чара сделать строку и вернуть элемент массива
	| isSep x = [x : (trim (takeWhile (isNotSep) xs))] ++ (splitPath $ dropWhile (isNotSep) xs)
	where
		isSep x = x `elem` ['m', 'l', 'z']
		isNotSep x = not $ isSep x




if __name__ == '__main__':
	print splitSvg(svg1)
#	show(svg1)
