import time
import sys

class ColoringPuzzle:
  def __init__(self,xsize,ysize,table):
    self.xsize = xsize
    self.ysize = ysize
    self.table = table
    self.number_completed = {}
    self.boxes = []
    self.numbers = {}
    self.numbers_todo = []

  def make_boxes(self):
    alku = time.time()
    lista = []
    for i in range(self.xsize):
      lista2 = []
      for j in range(self.ysize):
        lista2.append(Box(i,j))
      lista.append(lista2)
    loppu = time.time()
    self.boxes = lista

  def make_numbers(self):
    alku = time.time()
    all_numbers = {}
    for num in range(0,10):
      all_numbers[num] = []
      self.number_completed[num] = []
    for x in range(len(self.table)):
      y = 0
      for a in self.table[x]:
        if a == ';':
          y += 1
        else:
          boxes = []
          if x == 0 or y == 0 or x == (self.xsize-1) or y == (self.ysize-1):
            if x == 0:
              if y == 0:
                boxes.append(self.boxes[0][0])
                boxes.append(self.boxes[1][0])
                boxes.append(self.boxes[0][1])
                boxes.append(self.boxes[1][1])
              elif y == self.ysize-1:
                boxes.append(self.boxes[0][self.ysize-1])
                boxes.append(self.boxes[1][self.ysize-1])
                boxes.append(self.boxes[0][self.ysize-2])
                boxes.append(self.boxes[1][self.ysize-2])
              else:
                for i in range(y-1,y+2):
                  boxes.append(self.boxes[x][i])
                  boxes.append(self.boxes[x+1][i])
            elif x == self.xsize-1:
              if y == 0:
                boxes.append(self.boxes[self.xsize-1][0])
                boxes.append(self.boxes[self.xsize-2][0])
                boxes.append(self.boxes[self.xsize-1][1])
                boxes.append(self.boxes[self.xsize-2][1])
              elif y == self.ysize-1:
                boxes.append(self.boxes[self.xsize-1][self.ysize-1])
                boxes.append(self.boxes[self.xsize-1][self.ysize-2])
                boxes.append(self.boxes[self.xsize-2][self.ysize-1])
                boxes.append(self.boxes[self.xsize-2][self.ysize-2])
              else:
                for i in range(y-1,y+2):
                  boxes.append(self.boxes[x-1][i])
                  boxes.append(self.boxes[x][i])
            elif y == 0:
              for i in range(x-1,x+2):
                boxes.append(self.boxes[i][y])
                boxes.append(self.boxes[i][y+1])
            elif y == self.ysize-1:
              for i in range(x-1,x+2):
                boxes.append(self.boxes[i][y-1])
                boxes.append(self.boxes[i][y])
          else:
            for e in range((x-1),x+2):
              for r in range((y-1),y+2):
                boxes.append(self.boxes[e][r])
          new_number = Number(x,y,a,boxes)
          all_numbers[int(a)].append(new_number)
          self.boxes[x][y].set_number(new_number)
          for box in boxes:
            box.add_number_around(new_number)
    loppu = time.time()

    self.numbers = all_numbers

  def print_table(self, fileName):
    with open(fileName, 'w') as f:
      out = []
      for i in self.boxes:
        row = []
        for j in i:
          row.append(j.value)
        out.append(row)
      for i in out:
        print(i)
        for val in i:
          f.write(f'{val} ')
        f.write('\n')

  def solve_step_1(self):
    for num in self.numbers[0]:
      for box in num.number_boxes:
        box.value = 0
    for num in self.numbers[9]:
      for box in num.number_boxes:
        box.value = 1
    self.number_completed[0] = self.number_completed[0] + self.numbers[0]
    self.number_completed[9] = self.number_completed[9] + self.numbers[9]


  def solve_step_2(self):
    alku = time.time()
    for i in range(1,9):
      self.numbers_todo.extend(self.numbers[i])

    togo = True
    round = 1
    while togo is True:

      numbers_todo_round2 = self.numbers_todo.copy()
      togo = False
      print(f"step {round} heuristic {len(self.numbers_todo)}")
      for i in range(0,len(self.numbers_todo)):
        num = self.numbers_todo[i]
        boxes = num.number_boxes
        sum_black = 0
        sum_white = 0

        for box in boxes:
          if box.value == 1:
            sum_black += 1
          if box.value == 0:
            sum_white += 1

        if sum_black == num.n:
          for box in boxes:
            if box.value is None:
              box.value = 0
          numbers_todo_round2.remove(num)
          togo = True

        elif sum_white == (len(boxes)-int(num.n)+sum_black):
          for box in boxes:
            if box.value is None:
              box.value = 1
          numbers_todo_round2.remove(num)
          togo = True

        elif num.n == (len(boxes)-sum_white):
          for box in boxes:
            if box.value is None:
              box.value = 1
          numbers_todo_round2.remove(num)
          togo = True
      self.numbers_todo = numbers_todo_round2.copy()
      round += 1

    loppu = time.time()
    self.table_ready()

  def table_ready(self):
    if len(self.numbers_todo) == 0:
      return True
    else:
      return False

  def check_table(self):
    errors = []
    for i in self.boxes:
      for j in i:
        test = self.check_box(j)
        if test is not True:
          errors.extend(test)
    if len(errors) == 0:
      print('[SOLVED]')
    else:
      print('[FAILED]')
    for error in errors:
      print(f"{error.n} error at ({error.x}, {error.y})")

  def check_box(self,box):
    numbers_around = box.numbers_around
    result = True
    problem_numbers = []
    for number in numbers_around:
      black = 0
      white = 0
      for num_box in number.number_boxes:
        if num_box.value == 1:
          black += 1
        elif num_box.value == 0:
          white += 1
      if black > number.n:
        result =  False
        problem_numbers.append(number)
      elif white > (len(number.number_boxes)-black):
        result =  False
        problem_numbers.append(number)
    if result is True:
      return True
    else:
      return problem_numbers

  def solve_step_3(self,table):
    if table == 0:
      return table
    else:
      pass

class Box(ColoringPuzzle):
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.value = None
    self.number = None
    self.numbers_around = []

  def set_number(self,number):
    self.number = number
  
  def add_number_around(self,number):
    self.numbers_around.append(number)
  
class Number(ColoringPuzzle):
  def __init__(self,x,y,n,boxes):
    self.x = x
    self.y = y
    self.n = int(n)
    self.number_boxes = boxes

import numpy as np

def read(path):
    f = open(path, 'rt')
    h, w = [int(x) for x in f.readline().strip().split(' ')]
    mat = - np.ones((h, w), dtype=np.int32)
    for ih in range(h):
        iw = 0
        for it in f.readline().strip().split(' '):
            if it != '-1':
                mat[ih][iw] = int(it)
            iw += 1
    f.close()
    
    matrix = []
    for i in range(h):
        line = ''
        for j in range(w):
            if mat[i][j] == -1 or mat[i][j] == '.':
                if j<w-1:
                    line = line + ';'
                    continue
                elif j>=w-1: break
            elif mat[i][j] >=0 and mat[i][j] <=9:
                if j<w-1:
                    line = line + str(mat[i][j])
                    line = line + ';'
                elif j>=w-1:
                    line = line + str(mat[i][j])
            
        matrix.append(line)
    return h,w,matrix


if __name__ == "__main__":
  h,w,mat = read('input.txt')
  peli = ColoringPuzzle(h,w,mat)
  peli.make_boxes()
  peli.make_numbers()
  peli.solve_step_1()
  peli.solve_step_2()
  peli.print_table('output.txt')
  peli.check_table()