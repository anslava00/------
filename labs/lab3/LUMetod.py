from colorama import Fore

class LU:
    def __init__(self, file) -> None:
        self.A = [] #matrix a0, ..., aN, bi
        self.N = 0  #Count string NxN
        self.__ParsingFile(file)
        self.L = [[0.0 for j in range(self.N)] for i in range(self.N)]
        self.U = [[0.0 for j in range(self.N)] for i in range(self.N)]
        self.CalcLU()

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

    def CalcLU(self):
        for i in range(0, self.N):
            print(Fore.RED + "Step " + str(i))
            self.PrintALU()
            for j in range(0, self.N):
                Sum = 0.0
                for k in range(0, i):
                    Sum += self.L[i][k] * self.U[k][j]
                self.U[i][j] = self.A[i][j] - Sum
                if (i > j):
                    continue
                else:
                    Sum = 0.0
                    for k in range(0, i):
                        Sum += self.L[j][k] * self.U[k][i]
                    self.L[j][i] = (self.A[j][i] - Sum) / self.U[i][i]
        print(Fore.RED + "Step last")
        self.PrintALU()
        return 1

    def CalcRootL(self):
        for i in range(0, self.N):
            self.L[i].append(self.A[i][-1])
        for j in range(0, self.N - 1):
            for i in range(j + 1, self.N):
                self.L[i][j] *= self.L[j][-1]
            for k in range(0, j + 1):
                self.L[j + 1][-1] -= self.L[j + 1][k]
                self.L[j + 1][k] = 0
        print(Fore.RED + "Root for Matrix L" + Fore.WHITE)
        for i in range(0, self.N):
            print("l" + str(i + 1) + " = " + str(self.L[i][-1]))
        return [self.L[i][-1] for i in range(0, self.N)]

    def CalcRoot(self):
        RootL = self.CalcRootL()
        for i in range(0, self.N):
            self.U[i].append(RootL[i])
        for i in range(self.N - 1, -1, -1):
            Div = self.U[i][i]
            for j in range(i, self.N + 1):
                self.U[i][j] /= Div
            for j in range(i + 1, self.N):
                self.U[i][-1] -= self.U[i][j]
            for k in range(0, i):
                self.U[k][i] *= self.U[i][-1]
        return [self.U[i][-1] for i in range(0, self.N)]

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
        print(Fore.GREEN + caption + Fore.WHITE)
        for i in range(0, len(M)):
            for j in range(0, len(M[i])):
                if (i == j):
                    print(Fore.YELLOW + str(M[i][j]) + Fore.WHITE, end=" ")
                    continue
                if (j == self.N):
                    print(Fore.CYAN + str(M[i][j]) + Fore.WHITE, end=" ")
                    continue
                print(M[i][j], end=" ")
            print()

    def PrintALU(self):
        self.PrintMatrix(self.A, "Matrix A:")
        self.PrintMatrix(self.U, "Matrix U:")
        self.PrintMatrix(self.L, "Matrix L:")

def main():
    File = ["TestVchLab2.txt", "Test1.txt", "Test2.txt", "Test3.txt"]
    Matrix = LU('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\lab3\\' + File[1])
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