import tkinter as tk
import random
import time

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Space Invaders")
        self.geometry("1200x800")
        
         # Création du canvas
        self.canvas = tk.Canvas(self, width=1200, height=800)
        self.canvas.pack()

        # Chargement de l'image de fond
        self.background_image = tk.PhotoImage(file="photos/image_fond.png")

        # Ajout de l'image de fond au canvas
        self.background_image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        
        # Mise à jour de la taille de l'image de fond lorsque la fenêtre est redimensionnée
        
        
        # Mise en plein écran de la fenêtre
        self.state("zoomed")
        
        # Création du conteneur pour les boutons
        self.button_frame = tk.Frame(self.canvas, bg="#ffffff", bd=0)
        self.button_frame.place(relx=0.5, rely=0.5, anchor=tk.N)

        # Création des boutons
        self.play_button = tk.Button(self.button_frame, text="Jouer", command=self.on_play)
        self.play_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(self.button_frame, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.LEFT)

  
    def on_play(self):
        # Fermeture de la fenêtre actuelle
        self.destroy()
        # Création d'une nouvelle fenêtre
        game_window = GameWindow()

class GameWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ma fenêtre de jeu")
        self.geometry("1280x800")
        # Mise à jour de la taille de l'image de fond lorsque la fenêtre est redimensionnée
        
      
        # Mise en plein écran de la fenêtre
        self.state("zoomed")

        # Création du canvas
        self.canvas = tk.Canvas(self, width=1280, height=800)
        self.canvas.pack()

        # Chargement de l'image de fond
        self.background_image = tk.PhotoImage(file="photos/image_fond.png")

        # Création de l'image de fond
        self.background_label = self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)

        # Chargement de l'image du vaisseau
        self.ship_image = tk.PhotoImage(file="photos/ship.png")

        # Création du vaisseau
        self.ship_label = self.canvas.create_image(640, 640, image=self.ship_image)
        
        #chargement de l'image du tir
        self.shot_image = tk.PhotoImage(file="photos/shot.png")
        
        
        # Liage des évènements de touche de direction aux fonctions de déplacement du vaisseau
        self.bind("<Left>", self.move_ship_left)
        self.bind("<Right>", self.move_ship_right)
        self.bind("<KeyRelease>", self.stop_movement)
        self.bind("<r>", self.restart)
        self.bind("<q>", self.quit)
        #bind la touche r pour restart la partie
    
        # Liage de l'évènement de touche d'espace au tir du vaisseau
        self.bind("<space>", self.shoot)
        
        self.ship_speed = 12
        # Fait une liste vide pour compter les tirs
        self.shots = []
        self.shooting = False
        
        # Chargement de l'image de l'Alien
        self.alien_image = tk.PhotoImage(file="photos/alien.png")
        self.bullet_image = tk.PhotoImage(file = "photos/alien_shot.png")

        # Variable de l'Alien
        self.speed_alien = 3
        self.direction = "right"
        
        self.alien_width = self.alien_image.width()
        self.alien_height = self.alien_image.height()
        
        self.aliens = []
        for row in range(2):
            for col in range(8):
                x = col * self.alien_width + 100 + 30*col
                y = row * self.alien_height + 100 + 30*row
                alien = self.canvas.create_image(x, y, image=self.alien_image)
                self.aliens.append(alien)
                
        self.bullets = []  # Initialize the bullets list
        self.canvas.after(1000, self.random_alien_fire)
        self.move_alien()
        self.update_shot_position()
        self.move_alien_bullets()
        
     
        
        #Affichage du score
        self.score = 0
        self.score_text = tk.Text(self, font=("Arial", 20), bg="black", fg="white", width=10, height=1)
        self.score_text.place(x=150, y=10)
        self.score_text.insert(tk.END, "Score : " + str(self.score))
    
        #Affichage des vies
        self.lives = 3        
        self.lives_text = tk.Text(self, font=("TkDefaultFont", 20), bg="black", fg="white", width=10, height=1)
        self.lives_text.place(x=1200, y=10)
        self.lives_text.insert(tk.END, "Lives : " + str(self.lives))
        # Initialize the walls list and the hits counter
       
        self.x1_mur1, self.y1_mur1, self.x2_mur1, self.y2_mur1 = 200, 500, 500, 530
        self.rect1 = self.canvas.create_rectangle(self.x1_mur1, self.y1_mur1, self.x2_mur1, self.y2_mur1, fill='gray')
        self.x1_mur2, self.y1_mur2, self.x2_mur2, self.y2_mur2 = 800, 500, 1100, 530
        self.rect2 = self.canvas.create_rectangle(self.x1_mur2, self.y1_mur2, self.x2_mur2, self.y2_mur2, fill='gray')
        self.nb_hit_mur1 = 0
        self.nb_hit_mur2 = 0


    def random_alien_fire(self):
        self.bullets = []
        aliens_to_fire = random.sample(self.aliens, len(self.aliens)//3)
        # choose one random alien to fire
        for alien in aliens_to_fire: 
            x1, y1= self.canvas.coords(alien)
            bullet = self.canvas.create_image(x1, y1, image=self.bullet_image)
            self.bullets.append(bullet)
        self.move_alien_bullets()
        self.after(5000, self.random_alien_fire)

    def move_alien_bullets(self):
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, 10)
            bullet_bbox = self.canvas.bbox(bullet)
            ship_bbox = self.canvas.bbox(self.ship_label)
            if bullet_bbox[2] >= ship_bbox[0] and bullet_bbox[0] <= ship_bbox[2] and bullet_bbox[3] >= ship_bbox[1] and bullet_bbox[1] <= ship_bbox[3]:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                self.lives -= 1
                self.lives_text.delete(1.0, tk.END)
                self.lives_text.insert(tk.END, "Lives : " + str(self.lives))
                if self.lives == 0 :
                    self.game_over()
            elif bullet_bbox[3] > self.canvas.winfo_height():
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            elif (self.x1_mur1 <= bullet_bbox[0] <= self.x2_mur1 and self.y1_mur1 <= bullet_bbox[1] <= self.y2_mur1) or (self.x1_mur2 <= bullet_bbox[0] <= self.x2_mur2 and self.y1_mur2 <= bullet_bbox[1] <= self.y2_mur2):
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            elif (self.x1_mur1 <= bullet_bbox[0] <= self.x2_mur1 and self.y1_mur1 <= bullet_bbox[1] <= self.y2_mur1):
                self.nb_hit_mur1 += 1
                if (self.nb_hit_mur1 >= 3):
                    self.canvas.delete(self.rect1)
            elif (self.x1_mur2 <= bullet_bbox[0] <= self.x2_mur2 and self.y1_mur2 <= bullet_bbox[1] <= self.y2_mur2):
                self.nb_hit_mur2 += 1
                if (self.nb_hit_mur2 >= 3):
                    self.canvas.delete(self.rect2)
        self.after(140, self.move_alien_bullets)
     

    def move_alien(self):
        for alien in self.aliens:
            x, y = self.canvas.coords(alien)
            if self.direction == "right":
                self.canvas.move(alien, self.speed_alien, 0)
                if x > 1260 - 55:
                    self.direction = "left"
                    for a in self.aliens:
                        self.canvas.move(a, 0, 30)
            elif self.direction == "left":
                self.canvas.move(alien, -self.speed_alien, 0)
                if x < 20 + 55:
                    self.direction = "right"
                    for a in self.aliens:
                        self.canvas.move(a, 0, 30)
        self.after(10, self.move_alien)
    
    def move_ship_left(self, event):
        # Déplacement du vaisseau vers la gauche
        self.movement_direction = "left"
        self.move_ship()

    def move_ship_right(self, event):
        # Déplacement du vaisseau vers la droite
        self.movement_direction = "right"
        self.move_ship()

    def stop_movement(self, event):
        # Arrêt du déplacement du vaisseau
        self.movement_direction = None

    def move_ship(self):
        # Récupération de la position actuelle du vaisseau
        x, y = self.canvas.coords(self.ship_label)

        if self.movement_direction == "left":
            # Déplacement du vaisseau vers la gauche
            self.canvas.move(self.ship_label, -10, 0)

            # Vérification de la position du vaisseau pour empêcher qu'il ne sorte de la fenêtre
            if x < 0+55:
                self.canvas.move(self.ship_label, 10, 0)
        elif self.movement_direction == "right":
            # Déplacement du vaisseau vers la droite
            self.canvas.move(self.ship_label, 10, 0)
            
            #Verification de la position du vaisseau pour empêcher qu'il ne sorte de la fenêtre
            if x > 1280-55:
                self.canvas.move(self.ship_label, -10, 0)
   
        
    def shoot(self, event):
        # Récupération de la position du vaisseau
        x, y = self.canvas.coords(self.ship_label)
        # Création du tir a l'aide d'une image png
        shot = self.canvas.create_image(x, y, image=self.shot_image)
        
        # Vérifie que la liste self.shots ne contient pas déjà l'instance du tir créée
        if shot not in self.shots:
            # Ajout du tir à la liste des tirs 
            self.shots.append(shot) 
            # Mise à jour de la position du tir
            
    def update_shot_position(self):
        # Parcours de la liste des tirs et fait en sorte que la vitesse des tirs n'augmentent pas
        for shot in self.shots:
            x, y = self.canvas.coords(shot)
            self.canvas.move(shot, 0, -10)
            if y < 0:
                self.canvas.delete(shot)
                self.shots.remove(shot)
        # Rappel de la fonction pour mettre à jour la position des tirs
        self.after(10, self.update_shot_position)
        # vérifie si un tir a touché un alien
        for shot in self.shots:
            shot_x, shot_y = self.canvas.coords(shot)
            for alien in self.aliens:
                alien_x, alien_y = self.canvas.coords(alien)
                # vérifie si le tir est dans les limites de l'alien
                if (shot_x > alien_x - 30 and shot_x < alien_x + 30
                    and shot_y > alien_y - 30 and shot_y < alien_y + 30):
                    # le tir a touché l'alien, donc supprime le tir et l'alien
                    self.canvas.delete(shot)
                    self.shots.remove(shot)
                    self.canvas.delete(alien)
                    self.aliens.remove(alien)
                    self.score += 100
                    self.update_score()
                    # vérifie si il reste des aliens dans la liste, s'il n'y en a plus lance la fonction next_level
                    if len(self.aliens) == 0:
                        self.next_level()          
    
    def update_score(self):
        self.score_text.delete("1.0", tk.END)
        self.score_text.insert("1.0", f"Score: {self.score}")
    
    def game_over(self):
        self.canvas.delete("all")
        self.score_text.delete(1.0, "end")
        self.score_text.destroy()
        self.lives_text.delete(1.0, "end")
        self.lives_text.destroy(  )
        self.canvas.create_text(640, 360, text="Game Over", font=("Arial", 50), fill="red")
        self.canvas.create_text(640, 420, text=f"Score: {self.score}", font=("Arial", 50), fill="red")
        self.canvas.create_text(640, 480, text="Press R to restart", font=("Arial", 50), fill="red")
        self.canvas.delete(self.score_text)
        self.canvas.delete(self.lives_text)
        
    def restart(self, event):
        self.destroy()
        window = GameWindow()
        window.mainloop()
    
    def next_level(self):
        self.destroy()
        window = GameWindow2(self.score)
        window.mainloop()
        
    def quit(self, event):
        self.destroy()
         
        
class GameWindow2(tk.Tk):
    def __init__(self,score):
        tk.Tk.__init__(self)
        self.title("Ma fenêtre de jeu")
        self.geometry("1280x800")
        self.score = score
        
        
        # Mise en plein écran de la fenêtre
        self.state("zoomed")

        # Création du canvas
        self.canvas = tk.Canvas(self, width=1280, height=800)
        self.canvas.pack()

        # Chargement de l'image de fond
        self.background_image = tk.PhotoImage(file="photos/image_fond2.png")
          
        # Création de l'image de fond
        self.background_label = self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)

        # Chargement de l'image du vaisseau
        self.ship_image = tk.PhotoImage(file="photos/ship.png")

        # Création du vaisseau
        self.ship_label = self.canvas.create_image(640, 640, image=self.ship_image)
        
        #chargement de l'image du tir
        self.shot_image = tk.PhotoImage(file="photos/shot.png ")  
        
        
        # Liage des évènements de touche de direction aux fonctions de déplacement du vaisseau
        self.bind("<Left>", self.move_ship_left)
        self.bind("<Right>", self.move_ship_right)
        self.bind("<KeyRelease>", self.stop_movement)
        self.bind("<t>", self.restart)
        self.bind("<r>", self.restart2)
        self.bind("<q>", self.quit)
        
        #bind la touche r pour restart la partie
    
        # Liage de l'évènement de touche d'espace au tir du vaisseau
        self.bind("<space>", self.shoot)
        
        self.ship_speed = 12
        # Fait une liste vide pour compter les tirs
        self.shots = []
        self.shooting = False
        
        # Chargement de l'image de l'Alien
        self.alien_image = tk.PhotoImage(file="photos/alien2.png")
        self.bullet_image = tk.PhotoImage(file = "photos/alien_shot.png")

        # Variable de l'Alien
        self.speed_alien = 3
        self.direction = "right"
        
        self.alien_width = self.alien_image.width()
        self.alien_height = self.alien_image.height()
        
        self.aliens = []
        for row in range(3):
            for col in range(8):
                x = col * self.alien_width + 100 + 30*col
                y = row * self.alien_height + 100 + 30*row
                alien = self.canvas.create_image(x, y, image=self.alien_image)
                self.aliens.append(alien)
                
        self.bullets = []  # Initialize the bullets list
        self.canvas.after(1000, self.random_alien_fire)
        self.move_alien()
        self.update_shot_position()
        self.move_alien_bullets()
        
         
        #Affichage du score
        self.score_text = tk.Text(self, font=("Arial", 20), bg="black", fg="white", width=10, height=1)
        self.score_text.place(x=150, y=10)
        self.score_text.insert(tk.END, "Score : " + str(self.score))
    
        #Affichage des vies
        self.lives = 3        
        self.lives_text = tk.Text(self, font=("TkDefaultFont", 20), bg="black", fg="white", width=10, height=1)
        self.lives_text.place(x=1200, y=10)
        self.lives_text.insert(tk.END, "Lives : " + str(self.lives))
    
        #Affichage des murs
        self.x1_mur1, self.y1_mur1, self.x2_mur1, self.y2_mur1 = 200, 500, 500, 530
        self.rect1 = self.canvas.create_rectangle(self.x1_mur1, self.y1_mur1, self.x2_mur1, self.y2_mur1, fill='gray')
        self.x1_mur2, self.y1_mur2, self.x2_mur2, self.y2_mur2 = 800, 500, 1100, 530
        self.rect2 = self.canvas.create_rectangle(self.x1_mur2, self.y1_mur2, self.x2_mur2, self.y2_mur2, fill='gray')
        self.nb_hit_mur1 = 0
        self.nb_hit_mur2 = 0
        
    def random_alien_fire(self):       
        self.bullets = []
        aliens_to_fire = random.sample(self.aliens, len(self.aliens)//3)  # choose one random alien to fire
        for alien in aliens_to_fire: 
            x1, y1= self.canvas.coords(alien)
            bullet = self.canvas.create_image(x1, y1, image=self.bullet_image)
            self.bullets.append(bullet)
        self.move_alien_bullets()
        self.after(5000, self.random_alien_fire)

    def move_alien_bullets(self):
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, 10)
            bullet_bbox = self.canvas.bbox(bullet)
            ship_bbox = self.canvas.bbox(self.ship_label)
            if bullet_bbox[2] >= ship_bbox[0] and bullet_bbox[0] <= ship_bbox[2] and bullet_bbox[3] >= ship_bbox[1] and bullet_bbox[1] <= ship_bbox[3]:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                self.lives -= 1
                self.lives_text.delete(1.0, tk.END)
                self.lives_text.insert(tk.END, "Lives : " + str(self.lives))
                if self.lives == 0 :
                    self.game_over()
            elif bullet_bbox[3] > self.canvas.winfo_height():
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            elif (self.x1_mur1 <= bullet_bbox[0] <= self.x2_mur1 and self.y1_mur1 <= bullet_bbox[1] <= self.y2_mur1) or (self.x1_mur2 <= bullet_bbox[0] <= self.x2_mur2 and self.y1_mur2 <= bullet_bbox[1] <= self.y2_mur2):
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            elif (self.x1_mur1 <= bullet_bbox[0] <= self.x2_mur1 and self.y1_mur1 <= bullet_bbox[1] <= self.y2_mur1):
                self.nb_hit_mur1 += 1
                if (self.nb_hit_mur1 >= 3):
                    self.canvas.delete(self.rect1)
            elif (self.x1_mur2 <= bullet_bbox[0] <= self.x2_mur2 and self.y1_mur2 <= bullet_bbox[1] <= self.y2_mur2):
                self.nb_hit_mur2 += 1
                if (self.nb_hit_mur2 >= 3):
                    self.canvas.delete(self.rect2)
        self.after(140, self.move_alien_bullets)
     


    def move_alien(self):
        for alien in self.aliens:
            x, y = self.canvas.coords(alien)
            if self.direction == "right":
                self.canvas.move(alien, self.speed_alien, 0)
                if x > 1260 - 55:
                    self.direction = "left"
                    for a in self.aliens:
                        self.canvas.move(a, 0, 30)
            elif self.direction == "left":
                self.canvas.move(alien, -self.speed_alien, 0)
                if x < 20 + 55:
                    self.direction = "right"
                    for a in self.aliens:
                        self.canvas.move(a, 0, 30)
        self.after(10, self.move_alien)
    
    def move_ship_left(self, event):
        # Déplacement du vaisseau vers la gauche
        self.movement_direction = "left"
        self.move_ship()

    def move_ship_right(self, event):
        # Déplacement du vaisseau vers la droite
        self.movement_direction = "right"
        self.move_ship()

    def stop_movement(self, event):
        # Arrêt du déplacement du vaisseau
        self.movement_direction = None

    def move_ship(self):
        # Récupération de la position actuelle du vaisseau
        x, y = self.canvas.coords(self.ship_label)

        if self.movement_direction == "left":
            # Déplacement du vaisseau vers la gauche
            self.canvas.move(self.ship_label, -10, 0)

            # Vérification de la position du vaisseau pour empêcher qu'il ne sorte de la fenêtre
            if x < 0+55:
                self.canvas.move(self.ship_label, 10, 0)
        elif self.movement_direction == "right":
            # Déplacement du vaisseau vers la droite
            self.canvas.move(self.ship_label, 10, 0)
            
            #Verification de la position du vaisseau pour empêcher qu'il ne sorte de la fenêtre
            if x > 1280-55:
                self.canvas.move(self.ship_label, -10, 0)
   
        
    def shoot(self, event):
        # Récupération de la position du vaisseau
        x, y = self.canvas.coords(self.ship_label)
        # Création du tir a l'aide d'une image png
        shot = self.canvas.create_image(x, y, image=self.shot_image)
        
        # Vérifie que la liste self.shots ne contient pas déjà l'instance du tir créée
        if shot not in self.shots:
            # Ajout du tir à la liste des tirs 
            self.shots.append(shot) 
            # Mise à jour de la position du tir
            
    def update_shot_position(self):
        # Parcours de la liste des tirs et fait en sorte que la vitesse des tirs n'augmentent pas
        for shot in self.shots:
            x, y = self.canvas.coords(shot)
            self.canvas.move(shot, 0, -10)
            if y < 0:
                self.canvas.delete(shot)
                self.shots.remove(shot)
        # Rappel de la fonction pour mettre à jour la position des tirs
        self.after(10, self.update_shot_position)
        # vérifie si un tir a touché un alien
        for shot in self.shots:
            shot_x, shot_y = self.canvas.coords(shot)
            for alien in self.aliens:
                alien_x, alien_y = self.canvas.coords(alien)
                # vérifie si le tir est dans les limites de l'alien
                if (shot_x > alien_x - 30 and shot_x < alien_x + 30
                    and shot_y > alien_y - 30 and shot_y < alien_y + 30):
                    # le tir a touché l'alien, donc supprime le tir et l'alien
                    self.canvas.delete(shot)
                    self.shots.remove(shot)
                    self.canvas.delete(alien)
                    self.aliens.remove(alien)
                    self.score += 100
                    self.update_score()
                    if len(self.aliens) == 0:
                        self.game_won()
    
    def update_score(self):
        self.score_text.delete("1.0", tk.END)
        self.score_text.insert("1.0", f"Score: {self.score}")
    
    def game_over(self):
        self.canvas.delete("all")
        self.score_text.delete(1.0, "end")
        self.score_text.destroy()
        self.lives_text.delete(1.0, "end")
        self.lives_text.destroy(  )
        self.canvas.create_text(640, 360, text="Game Over", font=("Arial", 50), fill="red")
        self.canvas.create_text(640, 420, text=f"Score: {self.score}", font=("Arial", 50), fill="red")
        self.canvas.create_text(640, 480, text="Press T to restart", font=("Arial", 50), fill="red")
        
    #fait la fonction game_won en ajoutant un bouton quitter et un bouton restart 
    def game_won(self):
        self.canvas.delete("all")
        self.score_text.delete(1.0, "end")
        self.score_text.destroy()
        self.lives_text.delete(1.0, "end")
        self.lives_text.destroy(  )
        self.background_image = tk.PhotoImage(file="photos/image_victoire.png")

        # Création de l'image de fond
        self.background_label = self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)
        self.canvas.create_text(640, 360, text="You Won", font=("Arial", 50), fill="white") 
        self.canvas.create_text(640, 420, text=f"Score: {self.score}", font=("Arial", 50), fill="white")
        self.canvas.create_text(640, 480, text="Press R to restart", font=("Arial", 50), fill="white")
        self.canvas.create_text(640, 540, text="Press Q to quit", font=("Arial", 50), fill="white")
    
    def restart(self, event):
        self.destroy()
        window = GameWindow2(self.score)
        window.mainloop()
    def restart2(self, event):
        self.destroy()
        window = GameWindow()
        window.mainloop()
    def quit(self, event):
        self.destroy( )
         
if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()
 
