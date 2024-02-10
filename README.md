# platformer-game

## Goal

Get the hero to advance by accumulating the maximum score per level, by picking fruits and killing enemies. Clear all three levels to complete the stage.

## Pygame Concepts Utilized

### Sprite Sheet Components
- **Loading Spritesheet Components:** Used sprite sheets to efficiently manage and display multiple game sprites, which reduces memory usage and improves rendering performance.
### Player Movement
- **Moving the Player (Velocity/Gravity):** Implemented player movement using velocity and gravity, allowing realistic horizontal and vertical movement within the game world.
### Collision Detection
- **Pixel-Perfect Collision:** Employed pixel-perfect collision detection to ensure precise interaction between game entities for both shooting and collecting mechanics.
- **Rectangular Collision:** Implemented rectangular collision detection with pygame's built-in functions, enabling efficient detection and response to collisions between game entities, such as obstacles and objects.

## Controls

Use the 'A' and 'D' keys to move left and right, and press space to jump. In order to shoot, press the 'F' key.

## Functionalities

- **Double Jump:** Player's ability to perform a double jump, allowing them to reach higher platforms and evade obstacles with greater agility.
- **Collectible Items:** Added a variety of fruits scattered throughout the levels, each offering different score points when collected based on the size.
- **Health and Speed Potions:** Collectible potions that restore the player's health to maximum capacity. Additionally, a speed potion that temporarily boost the player's velocity for the duration of the level.
- **Enemies and Obstacles:** Navigate through challenging levels filled with diverse enemies to defeat. The larger the enemy, the more HP it has.
- **Interactive Shooting Mechanic:** Shooting bullets to eliminate enemies and obstacles. Shooting blocks or shooting off-screen removes the bullets.
- **Hit and Collect Animations:** Specific hit and collect animations for bullet-enemy and player-fruit collisions.
- **Working Sound Effects:** Fully functional sound effects, providing auditory feedback for actions and interactions.
- **Game Over Screen:** Dynamic game over screen upon dying, allowing players to restart the game upon clicking.

## Screenshots

![Start Screen](https://raw.githubusercontent.com/doriana2001/platformer-game/main/screenshots/start_screen.jpg)
![In-Game](https://raw.githubusercontent.com/doriana2001/platformer-game/main/screenshots/play_screen.jpg)
![Gameplay](https://raw.githubusercontent.com/doriana2001/platformer-game/main/screenshots/gameplay.gif)

## Credits

The following free resources were used in this project:

- **Sprites:** [Pixel Adventure by PixelFrog Assets](https://pixelfrog-assets.itch.io/pixel-adventure-1)
- **Bullet:** [Top Seller Game Assets: Bullet](https://itch.io/game-assets/top-sellers/tag-bullet)
- **Healthbar:** [Hearts and Health Bar by fliflifly](https://fliflifly.itch.io/hearts-and-health-bar?download%20health%20bar%20health%20bar)
- **Health Potion:** [Heart Shaped Potion Bottle by Lornent](https://lornent.itch.io/heart-shaped-potion-bottle)
- **Speed Potion:** [48 Free Magic Potions Pixel Art Icons by Free Game Assets](https://free-game-assets.itch.io/48-free-magic-potions-pixel-art-icons?download)
- **Sound Effects:** [Mixkit - Free Sound Effects: Game](https://mixkit.co/free-sound-effects/game/)
- **Start Button:** [Pixel Buttons by Humble Pixel](https://humblepixel.itch.io/pixel-buttons)
- **Score Font:** [Retro Gaming Font on Dafont.com](https://www.dafont.com/retro-gaming.font)
