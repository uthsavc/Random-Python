import math

################################################################################

### WHAT IS THIS 
# this is to test a variant of airplane problem
# the original problem goes like this: you have a 100 seat plane
# where each of the 100 passengers is assigned a seat. but the first passenger
# loses his boarding pass, and picks a seat at random. for each subsequent passenger
# they sit in their seat if its empty, and otherwise pick a seat at random. what's the
# probability the last passenger gets his own seat?

# anyway, one can also ask the following natural question: what's the expected num
# of passengers who aren't in their assigned seat? i conjectured (and proved) that the
# answer is the (n-1)-th Harmonic number, so I wrote something to test that for some small
# cases so I wouldn't have to do it by hand.

# i could of course dynamically program this by finding a clever recursion, but the problem
# with that is that the recursion is how i solved the problem! if i'm trying to test my answer
# i'll need to compute it naively.

################################################################################

# given n passengers, recursively computes the expected number of mismatched passengers
# P represents passengers
# L represents airplane seats
def airplane(n):
	P = list(range(1,n+1))
	L = list(range(1,n+1))
	sum=0
	for x in range(len(L)):
		if x==0:
			sum = sum + airplane_helper(P[1:],L[0:x]+L[(x+1):]) #picked the right seat!
		else: 
			sum=sum+(1/n)*(airplane_helper(P[1:],L[0:x]+L[(x+1):]) + 1) #uh oh picked the wrong seat
	return sum

# helper for above that does all the recursive work
# P is the passengers (numbered from 1 to n)
# L is the seats that are left (where seat i is passenger i's assigned seat)
def airplane_helper(P, L):
	if (len(P)==0): #no more passengers
		return 0
	else:
		toPick = P[0] #let's see what the first passenger who hasn't yet picked a seat will do
		if toPick in L: #is her seat available? if it is, give her her own seat
			i = L.index(toPick)
			j=i+1
			return airplane_helper(P[1:], L[0:i]+L[j:])
		else: #her seat isn't available so she picks a seat uniformly at random
			sum=0
			for x in range(len(L)):
				k=x+1
				sum=sum+(1/len(L))*(airplane_helper(P[1:], L[0:x]+L[k:])+1)
			return sum

# computes n-th harmonic number
def harmonic(n):
	if n==1:
		return 1
	else: 
		return ((1/n)+harmonic(n-1))

def check_airplane(n):
	eps = .0001
	works = True
	for x in range(3,n):
		works = works and (abs(harmonic(x-1)-airplane(x)) < eps)
	return works

print(check_airplane(20))