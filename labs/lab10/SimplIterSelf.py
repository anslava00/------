import copy
from numpy import dot, matrix, ones, transpose, zeros, shape, linalg
from colorama import Fore
class SimpleSelf:
    def __init__(self, file) -> None:
        self.A = [] #matrix a0, ..., aN, bi
        self.x = []
        self.accuracy = 10**-8
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

    def __sumModulY(self, y):
        sum = 0
        for i in range(self.N):
            sum += y[i, 0]**2
        return (sum)**0.5

    def __sgn(self, num):
        return 1 if num > 0 else -1

    def CalcRoot(self):
        A = matrix(self.A)[:, :-1]
        x = matrix(ones((self.N, 1)))
        k = 0
        while(True):
            y = dot(A, x)
            l = dot(transpose(y), x)
            modulY = self.__sumModulY(y)
            x0 = copy.deepcopy(x)
            x = y / modulY
            k += 1
            print(Fore.GREEN + "Iteration №" + str(k) + Fore.WHITE)
            self.PrintMatrix(y.tolist(), "|y| = " + str(modulY) + " | y : ")
            self.PrintMatrix(x.tolist(), "|l| = " + str(l[0, 0]) + " | x :")
            if (self.CheckAccuracy(x, x0, l)):
                break
        return transpose(x).tolist()[0], l.tolist()[0][0]

    def CheckAccuracy(self, x1, x0, l):
        for i in range(shape(x1)[0]):
            if (abs(self.__sgn(l) * x1[i, 0] - x0[i, 0]) > self.accuracy):
                return False
        return True

    def CheckOnTrue(self, l, lroot):
            w, v = linalg.eig(matrix(self.A)[:, :-1])
            print(Fore.CYAN + "NumPy self val = " + Fore.WHITE + str(sorted(w)))
            print(Fore.CYAN + "My self val = " + Fore.WHITE + str(l))
            print(Fore.YELLOW + "Difference : " + str(max(w) - l))
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
    File = ["test.txt", "1"]
    Matrix = SimpleSelf('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\labs\\lab10\\' + File[0])
    Matrix.PrintMatrix(Matrix.A, 'Matrix')
    lRoot, l = Matrix.CalcRoot()
    Matrix.CheckOnTrue(l, lRoot)

if __name__ == "__main__":
    main()
    