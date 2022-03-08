class MaxElements:
    def __init__(self, val, i, j) -> None:
        self.val = val
        self.i = i
        self.j = j

class ChooseGause:
    def __init__(self, file) -> None:
        self.M = [] #matrix a0, ..., aN, bi
        self.N = 0  #Count string NxN
        self.__ParsingFile(file)

    def __ParsingFile(self, file):
        F = open(file, 'r')
        self.N = int(F.readline())
        for iLine in range(0, self.N):
            Line = F.readline()
            self.M.append([])
            TmpString = ""
            for i in range(0, len(Line)):
                if (Line[i] == " " and not TmpString.isspace()):
                    self.M[-1].append(float(TmpString))
                    TmpString = ""
                else:
                    TmpString += Line[i]
            self.M[-1].append(float(TmpString))


    def CalcRoot(self):
        #A = self.M[0][0]
        #for i in range(0, self.N + 1):
        #    self.M[0][i] /= A
        for i in range(0, self.N):
            self.PrintMatrix()
            for d in range(0, i):
                DivElement = self.M[i][d]
                for j in range(0, self.N + 1):
                    self.M[i][j] -= self.M[d][j] * DivElement
            DiagElement = self.M[i][i]
            for j in range(i, self.N + 1):
                self.M[i][j] /= DiagElement
            for u in range(0, i):
                DivElement = self.M[u][i]
                for j in range(0, self.N + 1):
                    self.M[u][j] -= self.M[i][j] * DivElement
        self.PrintMatrix()
        return [[i, self.M[i][-1]]for i in range(0, self.N)]

        
    def PrintMatrix(self):
        print()
        for i in range(0, self.N):
            for j in range(0, self.N + 1):
                print(self.M[i][j], end=" ")
            print()
        print()

def main():
    File = ["Input3n3Ch", "Input4n4Ch", "Input3n3Op"]
    Matrix = ChooseGause('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\lab2\\' + File[0])
    Root = Matrix.CalcRoot()

    for i in range(0, len(Root)):
        print("x" + str(Root[i][0] + 1) + " = " + str(Root[i][1]))

if __name__ == "__main__":
    main()