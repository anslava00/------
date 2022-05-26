from numpy import dot, matrix, transpose, zeros, shape
from colorama import Fore
class Grad:
    def __init__(self, file) -> None:
        self.A = [] #matrix a0, ..., aN, bi
        self.x = []
        self.accuracy = 10**-4
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

    def CalcRoot(self):
        A = matrix(self.A)[:, :-1]
        b = matrix(self.A)[:, -1:]
        x = matrix(zeros((self.N, 1)))
        k = 0
        while(True):
            F = (dot(A, x) - b)
            r = -F
            if (self.CheckAccuracy(r)):
                break
            delta = (dot(transpose(r), r) / dot(transpose(r), dot(A, r)))[0, 0]
            x = x - delta * F
            k += 1
            self.PrintMatrix(x.tolist(), 'X on iteration ' + str(k))
        return transpose(x).tolist()[0]

    def CheckAccuracy(self, r):
        for i in range(shape(r)[0]):
            if (abs(r[i, 0]) > self.accuracy):
                return False
        return True

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
                print(Fore.GREEN + "  : " + str(Sum) + " : Ax === B: " + str(self.A[i][-1]) + Fore.WHITE)
        return F

    def PrintMatrix(self, M, caption = ""):
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
    File = ["test.txt", "1"]
    Matrix = Grad('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\labs\\lab8\\' + File[0])
    Matrix.PrintMatrix(Matrix.A, 'Matrix')
    Root = Matrix.CalcRoot()
    print(Root)
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
    