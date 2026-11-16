# Case do Dilemma 3mod: antes de imprimir

Combinado em 15/11/2026: o teclado será montado primeiro, e o case só será impresso depois, com as medidas reais.

## O que o case já tem

- **Bandeja** (parte de baixo): a placa fica apoiada em 9 colunas com porca M3 por baixo. Tem um rebaixo na frente para a chave liga/desliga.
- **Tampa**: cobre o controlador e a bateria (38 × 20 × 9 mm), que fica num compartimento na borda de dentro.
- **Entrada USB**: um rasgo em U na parede de trás, aberto até o topo da tampa. Serve para qualquer altura de pino.
- **Parafusos**: 5× M3×6 na bandeja, 4× M3×12 na tampa e 9 porcas M3. Para uma tampa mais alta, o script informa o tamanho certo do parafuso.
- Switches Choc, case reto (sem inclinação).
- Os arquivos atuais em `out/` são para um espaço de **2,5 mm** entre a placa e o controlador, o pino comum com o plástico.

## Medir depois de montar

1. **Espaço entre a placa do teclado e a placa do controlador**, em mm. Ele depende do pino usado: tenho pinos de dois tamanhos. É a altura do plástico preto do pino em que o controlador ficou apoiado.
   - até cerca de 1,9 mm: a tampa fica na altura das teclas (case com 14,6 mm);
   - 2,5 mm: a tampa fica 1,5 mm acima das teclas (16,1 mm);
   - mais que isso: a tampa sobe junto.
2. **Lado da entrada USB do controlador**: o case supõe que ela fica virada para a borda de **trás** da placa, como no desenho da PCB. Se ficar virada para o outro lado, o rasgo precisa mudar de lugar.
3. **Conector TRRS (J2)**: o case supõe que ele **não** foi soldado, porque ficaria no lugar da bateria. Se soldar, avisar.
4. **Bateria**: conferir que ela mede no máximo 38 × 20 × 9 mm, com os fios.
5. **Altura das teclas**: o case usa cerca de 8 mm do topo da placa até o topo da tecla Choc. Se as teclas forem diferentes, medir.

## Gerar os arquivos com a medida

Com o espaço medido (exemplo: 1,5 mm):

    python dilemma_case.py <dilemma.kicad_pcb> out 1.5
    python assembly.py <dilemma.kicad_pcb> preview 1.5

O Python com build123d ficava num ambiente temporário (`cadenv`, Python 3.12). Se ele tiver sido apagado, crie de novo com `python3.12 -m venv cadenv && cadenv/bin/pip install build123d matplotlib`. O arquivo da placa vem do repositório https://github.com/dixls/Dilemma-3mod (`dilemma/dilemma.kicad_pcb`).

Imprimir: `out/dilemma_tray_left.stl`, `dilemma_tray_right.stl`, `dilemma_cover_left.stl`, `dilemma_cover_right.stl`.
