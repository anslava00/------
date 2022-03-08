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
        self.MaxEl = self.__FindMaxElement()

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

    def __FindMaxElement(self):
        MaxElement = MaxElements(self.M[0][0], 0, 0)
        for i in range(0, self.N):
            for j in range(0, self.N):
                if (abs(self.M[i][j]) > abs(self.M[MaxElement.i][MaxElement.j])):
                    MaxElement.val = self.M[i][j]
                    MaxElement.i = i
                    MaxElement.j = j
        return MaxElement
    
    def __MakeGreenText(self, Text = '', End = ''):
        print("\033[32m {}".format(Text), end=End)
    def __MakeWhiteText(self, Text = '', End = ''):
        print("\033[37m {}".format(Text), end=End)
    def __MakeRedText(self, Text = '', End = ''):
        print("\033[31m {}".format(Text), end=End)

    def CalcRoot(self):
        MatrixRoot = []
        Mkof = [0 for i in range(self.N)]
        AKof = []
        for interation in range(0, self.N):
            self.PrintMatrix()
            MatrixRoot.append([self.MaxEl.j])
            for mi in range(0, len(Mkof)):
                if (mi != self.MaxEl.i):
                    Mkof[mi] = - self.M[mi][self.MaxEl.j]/self.M[self.MaxEl.i][self.MaxEl.j]
                else:
                    Mkof[mi] = 0
            print("M : " + str(Mkof))
             
            for i in range(0, self.N):
                for j in range(0, self.N + 1):
                    self.M[i][j] = self.M[i][j] + Mkof[i] * self.M[self.MaxEl.i][j]

            AKof.append([])
            for j in range(0, self.N + 1):
                AKof[-1].append(self.M[self.MaxEl.i][j]/self.MaxEl.val)
            print("A : " + str(AKof[-1]))
            for i in range(0, self.N):
                self.M[i][self.MaxEl.j] = 0
            for j in range(0, self.N + 1):
                self.M[self.MaxEl.i][j] = 0

            self.MaxEl = self.__FindMaxElement()
        
        print()
        for i in range(self.N - 1, -1, -1):
            for j in range(0, self.N):
                if (MatrixRoot[i][0] != j):
                    AKof[i][-1] -= AKof[i][j]
                    AKof[i][j] = 0
            for k in range(0, i):
                AKof[k][MatrixRoot[i][0]] *= AKof[i][-1]
            MatrixRoot[i].append(AKof[i][-1])

        for i in range(0, self.N):
            print(AKof[i])
    
        for i in range(self.N - 1):
            for j in range(self.N - 1 - i):
                if (MatrixRoot[j][0] > MatrixRoot[j + 1][0]):
                    MatrixRoot[j], MatrixRoot[j + 1] = MatrixRoot[j + 1], MatrixRoot[j]

        return MatrixRoot   

    def PrintMatrix(self):
        self.__MakeRedText(End="\n")
        for i in range(0, len(self.M)):
            for j in range(0, len(self.M[i])):
                self.__MakeRedText()
                if (self.MaxEl.i == i and self.MaxEl.j == j):
                    self.__MakeGreenText(self.M[i][j])
                    continue
                if (j == self.N):
                    self.__MakeWhiteText("| " + str(self.M[i][j]))
                    continue
                print(" " + str(self.M[i][j]), end="")
            print()
        self.__MakeWhiteText()

def main():
    File = ["Input3n3Ch", "Input4n4Ch", "Input3n3Op"]
    Matrix = ChooseGause('O:\\Lesson\\FileLesson\\ВЫЧМАТ\\lab2\\' + File[2])
    Root = Matrix.CalcRoot()

    for i in range(0, len(Root)):
        print("x" + str(Root[i][0] + 1) + " = " + str(Root[i][1]))

if __name__ == "__main__":
    main()