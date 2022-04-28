from cmath import sqrt
from tabnanny import check
from colorama import Fore
class Relax:
    def __init__(self, file) -> None:
        self.A = [] #matrix a0, ..., aN, bi
        self.accuracy = 10**-5
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

    def CalcRoot(self, w):
        # x0 = [self.A[i][-1]/self.A[i][i] for i in range(self.N)]
        x0 = [0 for i in range(self.N + 1)]
        Ax = []
        for i in range(self.N):
                Ax.append([self.A[i][-1] / self.A[i][i]])
                for j in range(self.N):
                    if (i != j):
                        Ax[i].append((self.A[i][j]) / self.A[i][i]) 
                    else:
                        Ax[i].append(0)
        k = 1
        while(True):
            x_0 = x0.copy()
            x1 = []
            for i in range(self.N):
                x1.append(Ax[i][0])
                for j in range(1, self.N + 1):
                    x1[i] -= (Ax[i][j] * x0[j - 1])
                x1[i] = w * (x1[i]) + x0[i] * (1 - w)
                x0[i] = x1[i]
            k += 1
            if (self.CheckAccuracy(x1, x_0)):
                x0 = x1[:]
                break
            x0 = x1[:]
        print(Fore.MAGENTA + 'for w = ' + str(w) + ' kol iteration = ' + str(k))
        return x0

    def CheckAccuracy(self, x1, x0):
        for i in range(len(x1)):
            if (abs(x1[i] - x0[i]) > self.accuracy):
                return False
        return True

    def CheckDiagDominate(self):
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
                    print(Fore.YELLOW + str(M[i][j]).center(pading, ' ') + Fore.WHITE, end=" ")
                    continue
                if (j == self.N):
                    print(Fore.CYAN + str(M[i][j]).center(pading, ' ') + Fore.WHITE, end=" ")
                    continue
                print(str(M[i][j]).center(pading, ' '), end=" ")
            print()

def checkRoot(Root, Matrix):
    if (Root):
        print(Fore.GREEN + "Root X : " + Fore.WHITE)
        for i in range(0, len(Root)):
            print("x" + str(i + 1) + " = " + str(Root[i]))
    print(Fore.GREEN + "Check on True" + Fore.WHITE)
    if (Matrix.CheckOnTrue(Root)):
        print(Fore.GREEN + "Roots is true" + Fore.WHITE)
    else:
        print(Fore.RED + "Roots is False" + Fore.WHITE)

def main():
    File = ["TestSimp.txt", "Test1.txt", "Testkv.txt", "1.txt"]
    Matrix = Relax('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\lab7\\' + File[3])
    Matrix.PrintMatrix(Matrix.A, 'Matrix')
    if (not Matrix.CheckDiagDominate()):
        return 0
    Root = []
    for w in range(1, 20):
        Root = Matrix.CalcRoot(w/10)
        # checkRoot(Root, Matrix)

if __name__ == "__main__":
    main()
    