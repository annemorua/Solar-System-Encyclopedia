# SOLAR SYSTEM ENCYCLOPEDIA
#### Video Demo: https://youtu.be/L8l52gUEhFc?si=7Z3Gr1LiKdhR3Hvq
#### Description:
This project consists of a graphical application created with Tkinter that allows users to explore and learn about the celestial bodies that make up the Solar System in an immersive way. The celestial bodies available for exploration are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, and the Sun. Below, the various features offered by the application are detailed:
- **Photo Collection**: :framed_picture:
  - In the form of a Polaroid-style photo, various images of the selected celestial body are displayed, which can be navigated forward with the right arrow or backward with the left arrow.
  - The images were sourced from the [NASA Science](https://science.nasa.gov/).
- **Physical and Orbital Data**: :page_with_curl:
  - Physical and orbital data of the various celestial bodies are presented in text format.
  - For physical information, each celestial body includes the same characteristics: average radius, surface area, volume, mass, surface gravity, and average temperature. The Sun, however, includes additional characteristics such as age and luminosity.
  - For orbital information, the planets have the following characteristics: orbital period, rotation period, and number of satellites. In the case of the Sun, the characteristics are: orbital period around the galactic center, rotation period, and average distance to the Milky Way's nucleus.
- **Gravitational Force**: :apple:
  - This section includes three features, the first of which simulates the free fall of two balls, comparing the gravitational acceleration between Earth and the selected celestial body.
  - It also includes two calculators: the first calculates the fall time of an object from a given height (in meters) using the equations of uniformly accelerated motion (MRUA), and the second calculates the final fall velocity from a given height, also in meters. If a non-numeric input is entered, or if a negative number is entered, a dialog box will appear with an error message.
- **Atmospheric Composition**: :test_tube:
  - The percentage of compounds present in the atmosphere of the celestial body is represented using filling bars. This percentage is visually shown through the height reached by the bars and numerically to indicate the exact value.

The program is designed to adjust to any screen size. Additionally, the input for entering the name of the celestial body is case-insensitive and ignores any extra spaces at the beginning or end. On the other hand, if an invalid input is entered, an error message will appear in a dialog box. If "the moon" is entered, a dialog box will inform the user that it is not yet available. The initial screen also features a help button to guide the user on how to begin exploring the celestial bodies, as well as an exit button to close the program. The frames displaying each of the celestial bodies are easily movable using the touchpad or mouse. Each frame includes an arrow-shaped button that quickly returns the user to the home screen, as well as an exit button to close the program. The functions can be executed as many times as desired, and the actions performed in each frame, as well as the position where the user left off, are preserved when returning to the home screen. This allows the user to make comparisons between planets without losing previous progress.
