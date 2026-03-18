init = function()
  x = 0
  y = 0
  screenHeight = 200
  screenWidht = 400
  shipsize=20
end

update = function()
  if keyboard.LEFT then x= x-2 end
  if keyboard.RIGHT then x= x+2 end
  if keyboard.UP then y= y+2 end
  if keyboard.DOWN then y= y-2 end
  
  local limitX = (screenWidht / 2) - (shipSize / 2)
  local limitY = (screenHeight / 2) - (shipSize / 2)
  
  if x > limitX then x = limitX end
  if x < -limitX then x = -limitX end
  if y > limitY then y = limitY end
  if y < -limitY then y = -limitY end
end

draw = function()
  screen.clear()
  screen.fillRect(0,0,screenWidht+20,screenHeight+20,"#468")
  screen.drawSprite("sprite",x,y,shipsize)
end