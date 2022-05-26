import copy
from numpy import column_stack, dot, matrix, ones, row_stack, transpose, zeros, shape, linalg
from colorama import Fore
class SimpleSelf:
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

    def __findA(self, y):
        max = 0
        for i in range(shape(y)[0]):
            if (y[i, 0] > max):
                max = y[i, 0]
        return max

    def __sgn(self, num):
        return 1 if num > 0 else -1

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
        return Ar1.tolist()

    def CalcRoot(self):
        A = matrix(self.A)[:, :-1]
        Ar = self.Okl()
        x = matrix(ones((self.N, 1)))

        a0 = self.__findA(x)

        k = 0
        while(True):
            x = dot(Ar, x / a0)
            a1 = self.__findA(x)
            l1 = 1 / a1
            
            k += 1
            print(Fore.GREEN + "Iteration №" + str(k) + Fore.WHITE)
            self.PrintMatrix(x.tolist(), "|l| = " + str(l1) + " | x :")
            if (self.CheckAccuracy(a1, a0)):
                break
            a0 = self.__findA(x)
        return transpose(x).tolist()[0], l1

    def CheckAccuracy(self, l1, l0):
        if (abs(1 / l1 - 1 / l0) > self.accuracy):
            return False
        return True

    def CheckOnTrue(self, l, lroot):
            w, v = linalg.eig(matrix(self.A)[:, :-1])
            print(Fore.CYAN + "NumPy self val = " + Fore.WHITE + str(sorted(w)))
            print(Fore.CYAN + "My self val = " + Fore.WHITE + str(l))
            print(Fore.YELLOW + "Difference : " + str(min(w) - l))
            self.PrintMatrix([lroot], "self vector for l = " + str(l))


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
    File = ["test.txt", "test2.txt"]
    Matrix = SimpleSelf('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\labs\\lab10\\' + File[0])
    Matrix.PrintMatrix(Matrix.A, 'Matrix')
    lRoot, l = Matrix.CalcRoot()
    Matrix.CheckOnTrue(l, lRoot)

if __name__ == "__main__":
    main()
    