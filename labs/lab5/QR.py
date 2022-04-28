from decimal import Rounded
from numpy import matrix, sqrt
import copy 
from colorama import Fore
class Sqrt:
    def __init__(self, file) -> None:
        self.A = [] #matrix a0, ..., aN, bi
        self.N = 0  #Count string NxN
        self.__ParsingFile(file)
        self.CopyA = copy.deepcopy(self.A)
        self.PrintMatrix(self.A, "Matrix A")
        self.CalcQR()

    def __ParsingFile(self, file):
        F = open(file, 'r')
        self.N = int(F.readline())
        for iLine in range(0, self.N):
            Line = F.readline()
            self.A.append([])
            TmpString = ""
            for i in range(0, len(Line)):
                if (Line[i] == " " and not TmpString.isspace()):
                    self.A[-1].append(float(TmpString))
                    TmpString = ""
                else:
                    TmpString += Line[i]
            self.A[-1].append(float(TmpString))

    def __SumP(self, k):
        sum = 0
        for l in range(k, self.N):
            sum += self.A[l][k]**2
        return sum

    def CalcQR(self):
        
        r = [0 for i in range(self.N)]
        q = 0
        for k in range(0, self.N - 1):
            P = [[0 for j in range(self.N + 1)] for i in range(self.N)]
            q = 1 if (self.A[k][k] >= 0) else -1
            P[k][k] = self.A[k][k] + q * sqrt(self.__SumP(k))
            for i in range(k, self.N):
                r[i] = P[k][k] * self.A[k][i + 1]
            for l in range(k + 1, self.N):
                P[l][k] = self.A[l][k]
                for i in range(k, self.N):
                    r[i] += P[l][k] * self.A[l][i + 1]
            s = 0
            for l in range(k, self.N):
                s += P[l][k]**2
            for i in range(k, self.N + 1):
                for j in range(k, self.N):
                    if (self.N != i):
                        P[j][i + 1] = 2*r[i]*P[j][k]/s
                    self.A[j][i] -= P[j][i]
            print(Fore.RED + "Step " + str(k) +Fore.WHITE)
            self.PrintMatrix(P, "Matrix P")
            self.PrintMatrix(self.A, "Matrix A")
            
    def CalcRoot(self):
        for i in range(self.N - 1, -1, -1):
            Div = self.A[i][i]
            for j in range(i, self.N + 1):
                self.A[i][j] /= Div
            for j in range(i + 1, self.N):
                self.A[i][-1] -= self.A[i][j]
            for k in range(0, i):
                self.A[k][i] *= self.A[i][-1]
        return [self.A[i][-1] for i in range(0, self.N)]

    def CheckOnTrue(self, root):
        F = True
        for i in range(0, self.N):
            Sum = 0.0
            for j in range(0, self.N):
                Sum += self.CopyA[i][j] * root[j]
                print(str(self.CopyA[i][j]) + " * " + str(root[j]), end="")
                if (j != self.N - 1):
                    print(" + ", end="")
            Rd = len(str(self.CopyA[i][-1]))
            if (round(Sum, Rd) != self.CopyA[i][-1]):
                F = False
                print(Fore.RED + "  : " + str(round(Sum, Rd)) + " : Ax === B: " + str(self.CopyA[i][-1]) + Fore.WHITE)
            else:
                print(Fore.GREEN + "  : " + str(round(Sum, Rd)) + " : Ax === B: " + str(self.CopyA[i][-1]) + Fore.WHITE)
        return F

    def PrintMatrix(self, M, caption = ""):
        Pading = 0
        for i in range(0, len(M)):
            for j in range(0, len(M[i])):
                if (len(str(M[i][j])) > Pading):
                    Pading = len(str(M[i][j]))
        print(Fore.GREEN + caption + Fore.WHITE)
        for i in range(0, len(M)):
            for j in range(0, len(M[i])):
                if (i == j):
                    print(Fore.YELLOW + str(M[i][j]).center(Pading, ' ') + Fore.WHITE, end=" ")
                    continue
                if (j == self.N):
                    print(Fore.CYAN + str(M[i][j]).center(Pading, ' ') + Fore.WHITE, end=" ")
                    continue
                print(str(M[i][j]).center(Pading, ' '), end=" ")
            print()


def main():
    File = ["Test1.txt", "TestVchLab2.txt", "GS.txt"]
    Matrix = Sqrt('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\lab5\\' + File[1])
    Matrix.PrintMatrix(Matrix.A, "Matrix A after : ")
    Root = Matrix.CalcRoot()
    if (Root):
        print(Fore.GREEN + "Root X : " + Fore.WHITE)
        for i in range(0, len(Root)):
            print("x" + str(i + 1) + " = " + str(Root[i]))
    print(Fore.GREEN + "Check on True" + Fore.WHITE)
    if (Matrix.CheckOnTrue(Root)):
        print(Fore.GREEN + "Roots is true" + Fore.WHITE)
    else:
        print(Fore.RED + "Roots is False" + Fore.WHITE)

if __name__ == "__main__":
    main()
