from cmath import cos, pi
import copy
from colorama import Fore
from numpy import dot, matrix, ones, zeros, shape, linalg, transpose
class Simple:
    def __init__(self, file) -> None:
        self.A = [] #matrix a0, ..., aN, bi
        self.accuracy = 10**-3
        self.N = 0  #Count string NxN
        self.__ParsingFile(file)

    def __ParsingFile(self, file):
        F = open(file, 'r')
        self.N = int(F.readline())
        for iLine in range(0, self.N):
            line = F.readline()
            self.A.append([])
            tmpString = ""
            for i in range(0, len(line)):
                if (line[i] == " " and not tmpString.isspace()):
                    self.A[-1].append(float(tmpString))
                    tmpString = ""
                else:
                    tmpString += line[i]
            self.A[-1].append(float(tmpString))

    def __findMaxNoDiag(self, A):
        maxI, maxJ = 0, 1
        for i in range(self.N):
            for j in range(self.N):
                if (i != j and A[i, j] > A[maxI, maxJ]):
                    maxI = i
                    maxJ = j
        return maxI, maxJ

    def __sgn(self, num):
        return 1 if num > 0 else -1

    def calcSelfMeans(self, p):
        tau = [10**(-(i)) for i in range(1, p + 1)]
        A = matrix(self.A[:])[ :, :-1]
        
        T = zeros((self.N, self.N))
        for i in range(self.N):
            T[i, i] = 1

        for q in range(p):
            i, j = self.__findMaxNoDiag(A)
            while(abs(A[i, j]) >= tau[q]):
                d = ((A[i, i] - A[j, j])**2 + 4 * (A[i, j]**2))**0.5
                c = (0.5 * (1 + abs(A[i, i] - A[j, j]) / d))**0.5
                s = (self.__sgn(A[i, j] * (A[i, i] - A[j, j])) *
                        (0.5 * (1 - abs(A[i, i] - A[j, j]) / d))**0.5)

                Tij = zeros((self.N, self.N))
                for t in range(self.N):
                    Tij[t, t] = 1
                Tij[i, i], Tij[j, j] = c, c
                Tij[i, j], Tij[j, i] = -s, s
                T = dot(T, Tij)
            
                newA = A.copy()
                newA[i, j], newA[j, i] = 0, 0

                for k in range(self.N):
                    if(k == i or k == j):
                        continue
                    newA[i, k] = c * A[k, i] + s * A[k, j]
                    newA[k, i] = newA[i, k]

                    newA[j, k] = -s * A[k, i] + c * A[k, j]
                    newA[k, j] = newA[j, k]
                newA[i, i] = c*c * A[i, i] + 2 * c * s * A[i, j] + s*s *A[j, j]
                newA[j, j] = s*s * A[i, i] - 2 * c * s * A[i, j] + c*c * A[j, j]

                A = newA
                
                print(str(i) + " == " + str(j))
                self.printMatrix(A.tolist(), 'Matrix on ' + str(tau[q]) + ' tau:')
                i, j = self.__findMaxNoDiag(A)
            
        return matrix([A[i, i] for i in range(self.N)]), T

    def checkSelfMeans(self, sM, sVM):
        print(Fore.GREEN + "Check self val" + Fore.WHITE)
        A = matrix(self.A)[:, :-1]
        w, v = linalg.eig(A)
        print(Fore.CYAN + "NumPy self val = " + Fore.WHITE + str(sorted(w)))
        print(Fore.CYAN + "My self val = " + Fore.WHITE + str(sM[0, :]))

    def selfMinMax(self, selfMeans):
        minI, maxI = 0, 0
        for i in range(1, shape(selfMeans)[1]):
            if (selfMeans[0, minI] > selfMeans[0, i]):
                minI = i
            if (selfMeans[0, maxI] < selfMeans[0, i]):
                maxI = i

        return selfMeans[0, maxI], selfMeans[0, minI]

    def calcRoot(self, p):
        selfMeans, selfVectorMeans = self.calcSelfMeans(p)
        self.printMatrix(selfMeans.tolist(), 'Self value:')
        self.printMatrix(selfVectorMeans.tolist(), 'Self vector value:')
        self.checkSelfMeans(selfMeans, selfVectorMeans)

        lMax, lMin = self.selfMinMax(selfMeans)
        # x0 = zeros((self.N, 1))
        x0 = matrix([[2],[2.5]])
        eta = lMin / lMax
        ro = (1 - eta) / (1 + eta)
        tau0 = 2 / (lMin + lMax)

        b = matrix(self.A)[: , -1]
        A = matrix(self.A[:])[ :, :-1]
        u = 0
        while(True):
            u += 1
            x1 = 0
            print(Fore.GREEN + "New Iteration " + str(u) + Fore.WHITE)
            print(x0)
            block =11
            for k in range(1, block):
                vk = cos((2 * k - 1) * pi / (2 * (block - 1))).real
                tauK = (tau0 / (1 + ro * vk)).real

                if (k == block - 1):
                    x1 = copy.deepcopy(x0)
                x0 = ((b - dot(A, x0)) * tauK + x0)
            if (self.CheckAccuracy(x1, x0)):
                break
        print(Fore.GREEN + "New Iteration " + str(u + 1) + Fore.WHITE)
        print(x0)
        return transpose(x0).tolist()[0]

    def CheckAccuracy(self, x1, x0):
        for i in range(shape(x1)[0]):
            if (abs(x1[i, 0] - x0[i, 0]) > self.accuracy):
                return False
        return True

    def checkDiagDominate(self):
        for i in range(self.N):
            sum = 0
            for j in range(self.N):
                if (i != j):
                   sum += self.A[i][j]
            if (abs(self.A[i][i]) < sum):
                print(Fore.RED + "Diagonal is not dominate" + Fore.WHITE)
                return False
        print(Fore.GREEN + "Diagonal is dominate" + Fore.WHITE)
        return True 

    def checkOnTrue(self, root):
        F = True
        for i in range(0, self.N):
            Sum = 0.0
            for j in range(0, self.N):
                Sum += self.A[i][j] * root[j]
                print(str(self.A[i][j]) + " * " + str(root[j]), end="")
                if (j != self.N - 1):
                    print(" + ", end="")
            Rd = len(str(self.A[i][-1]))
            if (round(Sum, Rd) != self.A[i][-1]):
                F = False
                print(Fore.RED + "  : " + str(round(Sum, Rd)) + " : Ax === B: " + str(self.A[i][-1]) + Fore.WHITE)
            else:
                print(Fore.GREEN + "  : " + str(Sum) + " : Ax === B: " + str(self.A[i][-1]) + Fore.WHITE)
        return F

    def printMatrix(self, M, caption = ""):
        pading = 0
        for i in range(0, len(M)):
            for j in range(0, len(M[i])):
                if (len(str(M[i][j])) > pading):
                    pading = len(str(M[i][j]))
        print(Fore.GREEN + caption + Fore.WHITE)
        for i in range(0, len(M)):
            for j in range(0, len(M[i])):
                if (i == j):
                    print(Fore.YELLOW + str(round(M[i][j], 10)).center(pading, ' ') + Fore.WHITE, end=" ")
                    continue
                if (j == self.N):
                    print(Fore.CYAN + str(round(M[i][j], 10)).center(pading, ' ') + Fore.WHITE, end=" ")
                    continue
                print(str(round(M[i][j], 10)).center(pading, ' '), end=" ")
            print()


def main():
    p = 5
    file = ["test1.txt", "test2.txt", "test3.txt"]
    matrix = Simple('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\labs\\lab9\\' + file[0])
    matrix.printMatrix(matrix.A, 'matrix')
    # if (not matrix.checkDiagDominate()):
    #     return 0
    Root = matrix.calcRoot(p)
    if (Root):
        print(Fore.GREEN + "Root X : " + Fore.WHITE)
        for i in range(0, len(Root)):
            print("x" + str(i + 1) + " = " + str(Root[i]))
    print(Fore.GREEN + "Check on True" + Fore.WHITE)
    if (matrix.checkOnTrue(Root)):
        print(Fore.GREEN + "Roots is true" + Fore.WHITE)
    else:
        print(Fore.RED + "Roots is False" + Fore.WHITE)

if __name__ == "__main__":
    main()
    