                for circ in TD_circs:
                    if circ.collidepoint(enemy):
                        index = TD_circs.index(circ)
                        try:
                            if index >=0:
                                pygame.draw.rect(screen, TD_darkGreen, colorRects[index], width=0)
                                guardW = TD_guardRects[index][0]
                                guardH = TD_guardRects[index][1]
                                screen.blit(guard,[guardW,guardH])
                        except:
                            pass
                        wdthStart = circ[0] + circ[2]/2
                        hghtStart = circ[1] + circ[3]/2
                        if index>=0:
                            pygame.draw.line(screen, red, [wdthStart,hghtStart], enemy, 3) 