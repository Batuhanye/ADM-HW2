#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 22:36:51 2019

@author: ujafarli
"""
# Theoretical question part 1 - Running time

function splitSwap(a, l, n):
    if n <= 1:                                 # run 1 time to check n
        return                                 # run 1 time
          splitSwap(a, l, n/2)                 # run n/2 time
          splitSwap(a, l+ n /2, n/2)           # run n/2 time
          swapList(a, l, n)                    # run 2n time
  
  
function swapList(a, l, n):
    for i = 0 to n/2:                          # run n/2
        tmp = a[l + i]                         # run n/2
        a[l + i] = a[l + n/2 + i]              # run n/2
        a[l + n/2 + i] = tmp                   # run n/2
        
        
 """       
# Overall 1 + 1 + n/2 + n/2 + 2n = 3n + 2 running time
# Running time of SplitSwap is O(n) which is linear
 """     
# Theoretical question part 2 
"""
Function splitSwap takes array a and if the lenght is greater than 1 divide it into 2 part:
from 1 to n/2 is new array 1 and from n/2+1 to n is new array 2. It is a recursive function
and every time new arrays divided into 2 part aswell. In addition, after each division, this
2 arrays swap places with each other. At the end we got reversed order of given array a

Example: a = [1,2,3,4,5,6,7,8]
devide it a1 = [1,2,3,4] a2 = [5,6,7,8] 
          a11 = [1,2]  a12 = [3,4]
          a21 = [5,6]  a22 = [7,8]  
          a211 = [5] a212 = [6] a221 = [7] a222 = [8]
          a111 = [1] a112 = [2] a121 = [3] a122 = [4]
          Swap them:
          a111 swap with a112:a11= [2,1]
          a121 swap with a122 a12= [4,3]
          a11  swap with a12  a1==> [4,3,2,1]
          ***
          a211 swap with a212:a21= [6,5]
          a221 swap with a222 a22= [8,7]
          a21  swap with a22  a2==> [8,7,6,5]
          ***
          At the end swap a1 and a2 ==> [8,7,6,5,4,3,2,1]
          
It is O(n), it is optimal.. But logn is more optimal than O(n)

"""
        