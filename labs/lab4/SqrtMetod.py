from sympy import sqrt
from colorama import Fore
class Sqrt:
    def __init__(self, file, Range = 100) -> None:
        self.RangeVal = Range
        self.A = [] #matrix a0, ..., aN, bi
        self.N = 0  #Count string NxN
        self.__ParsingFile(file)
        self.L = [[0.0 for j in range(self.N + 1)] for i in range(self.N)]
        self.CalcL()

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

    def __SumS(self, i, j):
        sum = 0
        for k in range(0, i):
            sum += self.L[k][i] * self.L[k][j]
        return sum

    def CalcL(self):
        for i in range(0, self.N):
            self.L[i][i] = sqrt(self.A[i][i] - self.__SumS(i, i))
            for j in range(i + 1, self.N + 1):
                self.L[i][j] = (self.A[i][j] - self.__SumS(i, j)) / self.L[i][i]

    def CalcRoot(self):
        for i in range(self.N - 1, -1, -1):
            Div = self.L[i][i]
            for j in range(i, self.N + 1):
                self.L[i][j] /= Div
            for j in range(i + 1, self.N):
                self.L[i][-1] -= self.L[i][j]
            for k in range(0, i):
                self.L[k][i] *= self.L[i][-1]
        return [self.L[i][-1] for i in range(0, self.N)]

    def CheckOnTrue(self, root):
        F = True
        for i in range(0, self.N):
            Sum = 0.0
            for j in range(0, self.N):
                Sum += self.A[i][j] * root[j]
                print(str(self.A[i][j]) + " * " + str(root[j]), end="")
                if (j != self.N - 1):
                    print(" + ", end="")
            if (Sum != self.A[i][-1]):
                F = False
                print(Fore.RED + "  := " + str(Sum) + " = " + str(self.A[i][-1]) + Fore.WHITE)
            else:
                F = True
                print(Fore.GREEN + "  := " + str(Sum) + " = " + str(self.A[i][-1]) + Fore.WHITE)
            
        return F

    def PrintMatrix(self, M, caption = ""):
        Pading = 0
        for i in range(0, len(M)):
            for j in range(0, len(M[i])):
                if (len(str(M[i][j])) > Pading):
                    Pading = len(str(M[i][j]))
        print(Pading)
        print(Fore.GREEN + caption + Fore.WHITE)
        for i in range(0, len(M)):
            for j in range(0, len(M[i])):
                if (i == j):
                    print(Fore.YELLOW + str(M[i][j]).center(Pading , ' ') + Fore.WHITE, end=" ")
                    continue
                if (j == self.N):
                    print(Fore.CYAN + str(M[i][j]).center(Pading, ' ') + Fore.WHITE, end=" ")
                    continue
                print(str(M[i][j]).center(Pading, ' '), end=" ")
            print()


def main():
    File = ["Test1.txt"]
    Matrix = Sqrt('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\lab4\\' + File[0])
    Matrix.PrintMatrix(Matrix.A, "Matrix A : ")
    Matrix.PrintMatrix(Matrix.L, "Matrix L  before:")
    Root = Matrix.CalcRoot()
    Matrix.PrintMatrix(Matrix.L, "Matrix L after:")
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