import 'package:flutter/material.dart';

class MealResultScreen extends StatelessWidget {
  const MealResultScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // Use a white scaffold so content looks like your screenshot
      backgroundColor: Colors.white,
      // keep the app bar similar to camera screen
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_none, color: Colors.black),
            onPressed: () {},
          ),
        ],
      ),

      // Main content
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Your Meal",
              style: TextStyle(fontSize: 34, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),

            const Text("• Shredded chicken with black beans : 1/2 cup\n  ~147 calories"),
            const Text("• Green peas: 1/4 cup\n  ~29 calories"),
            const Text("• Corn: 1/4 cup\n  ~33 calories"),

            const SizedBox(height: 20),

            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image(
                image: AssetImage("assets/meal.jpg"),
                height: 260,
                width: double.infinity,
                fit: BoxFit.cover,
                // if you don't have the asset, it will throw — replace or remove if needed
              ),
            ),

            const SizedBox(height: 20),

            const Text(
              "Yay, you have successfully planned a nutritious and flavorful toddler meal with the right portion sizes and essential vitamins!",
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 12),
            const Text(
              "40–50% of daily vitamin C\n"
              "45–55% of daily vitamin K\n"
              "20–25% of daily folate\n"
              "20–40% of several B vitamins\n"
              "15–30% of daily iron\n\n"
              "It also supplies a good amount of protein and fiber to support healthy growth and development.",
              style: TextStyle(fontSize: 16),
            ),

            const SizedBox(height: 20),

            const Text(
              "Keep offering a variety of foods like this to help meet your toddler’s nutritional needs!",
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 60),
          ],
        ),
      ),

      // <-- NEW FOOTER (so icons appear on this screen as well) -->
      bottomNavigationBar: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: const BoxDecoration(
          color: Colors.white,
          border: Border(top: BorderSide(color: Colors.black12)),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            const Icon(Icons.grid_view_rounded, size: 28),
            const Icon(Icons.chat_bubble_outline, size: 28),

            // Large camera button in footer (you can hook this to an action)
            Container(
              padding: const EdgeInsets.all(5),
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Color(0xFFDFF8FF),
              ),
              child: Container(
                height: 65,
                width: 65,
                decoration: const BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.white,
                ),
                child: IconButton(
                  icon: const Icon(Icons.camera_alt, size: 32),
                  onPressed: () {
                    // Example: go back to CameraScreen
                    Navigator.pop(context);
                  },
                ),
              ),
            ),

            const Icon(Icons.bookmark_border, size: 28),
            const Icon(Icons.person_outline, size: 28),
          ],
        ),
      ),
    );
  }
}
