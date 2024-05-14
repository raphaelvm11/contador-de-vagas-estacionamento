import cv2
import numpy as np

#cordenada dasa vagas para demarar(so ir testando)
vaga1 = [1, 89, 108, 213]
vaga2 = [115, 87, 152, 211]
vaga3 = [289, 89, 138, 212]
vaga4 = [439, 87, 135, 212]
vaga5 = [591, 90, 132, 206]
vaga6 = [738, 93, 139, 204]
vaga7 = [881, 93, 138, 201]
vaga8 = [1027, 94, 147, 202]
vaga9 = [1190, 95, 108, 204]

#variavel que junta tds as vagas pra não precisar colocar uma por uma e o code ficar pequeno
vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8, vaga9]

#importando o video para o projeto
video = cv2.VideoCapture('video.mp4')

#gerando as imagens(video, imagem em preto e branco para pegar os pixels pretos)
while True:
    check,img = video.read()
    imgCinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgBlur = cv2.medianBlur(imgTh,5)
    kernel = np.ones((3,3), np.int8)
    imgDil = cv2.dilate(imgBlur,kernel)

    #tem que ser 0 para contabilizar 1 carro
    quantVagasDesoc = 0
    for x,y,w,h in vagas:
        recorte = imgDil[y:y+h, x:x+w]
        quantPxBranco = cv2.countNonZero(recorte)
        cv2.putText(img,str(quantPxBranco),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
        
        #se a qtd de px branco for maior que 3k(so fica 3k se tiver o carro la dentro) ai o retangulo fica vermelho
        if quantPxBranco > 3000:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
        #se não for, o retangulo continua verde
        else:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            #isso faz com que se o carro entrar na vaga diminua 1 nas vagas desocupadas, se colocar 2 o carro vai contar como se ocupasse 2 vagas e vai dobrar a qtd
            quantVagasDesoc += 1
    
    #aqui diz q se o retangulo for ocupado ele vai contar
    cv2.rectangle(img,(90,0),(415,60),(255,0,0),-1)
    #aqui coloca o txt com a qtd de carros e vagas la em cima e a cor dele
    cv2.putText(img,f'LIVRE: {quantVagasDesoc}/9',(95,45),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),5)

    #aqui faz aparecer as imagens, se n tiver não aparece as img
    cv2.imshow('video', img)
    cv2.imshow('video TH', imgTh)
    #aqui deixa o video mais lento ou mais rapido
    cv2.waitKey(5)
