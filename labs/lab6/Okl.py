from numpy import array, column_stack, dot, matrix, row_stack
from colorama import Fore
class Okl:
    def __init__(self, file) -> None:
        self.A = [] #matrix a0, ..., aN, bi
        self.Ar1 = []
        self.N = 0  #Count string NxN
        self.__ParsingFile(file)
        self.PrintMatrix(self.A, "Matrix A")
        self.Okl()

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
            
    def Okl(self):
        A = matrix(self.A)[:,:self.N]
        Ar1 = 1 / A[:1,:1]
        for k in range(1, self.N):
            V = A[k, : k]
            U = A[ : k, k]
            ak = (A[k, k] - dot(dot(V,Ar1), U))[0, 0]
            rk = dot(-1/ak, dot(Ar1, U))
            qk = dot(-1/ak,dot(V, Ar1))
            B = Ar1 - dot(dot(Ar1, U), qk)
            Ar1 = (row_stack(
                (column_stack((B, rk)),column_stack((qk, 1/ak)))
                ))
            print(Fore.RED + "Step: " + str(k) + Fore.WHITE)
            self.PrintMatrix(Ar1.tolist(), 'Ret matrix')
        self.Ar1 = Ar1.tolist()

    def CalcRoot(self):
        B = array(self.A)[:, self.N:]
        Ar1 = array(self.Ar1)
        return dot(Ar1, B)[:,0].tolist()

    def CheckOnTrue(self, root):
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
                print(Fore.GREEN + "  : " + str(round(Sum, Rd)) + " : Ax === B: " + str(self.A[i][-1]) + Fore.WHITE)
        return F

    def CheckReturnMatrix(self, A, Ar1):
        A = array(A)[:, :self.N]
        Ar1 = array(Ar1)
        self.PrintMatrix(dot(A, Ar1), "Matrix A*A^1")
        self.PrintMatrix(dot(Ar1, A), "Matrix A^1*A")

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
                    print(Fore.YELLOW + str(round(M[i][j], 10)).center(Pading, ' ') + Fore.WHITE, end=" ")
                    continue
                if (j == self.N):
                    print(Fore.CYAN + str(round(M[i][j], 10)).center(Pading, ' ') + Fore.WHITE, end=" ")
                    continue
                print(str(round(M[i][j], 10)).center(Pading, ' '), end=" ")
            print()


def main():
    File = ["Okl.txt", "Testgs.txt", "Testkv.txt"]
    Matrix = Okl('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\lab6\\' + File[1])
    Matrix.PrintMatrix(Matrix.A, 'Matrix')
    Matrix.PrintMatrix(Matrix.Ar1, 'Return Matrix')
    Matrix.CheckReturnMatrix(Matrix.A, Matrix.Ar1)
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