import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: CameraMealScreen(),
    );
  }
}

class CameraMealScreen extends StatefulWidget {
  const CameraMealScreen({super.key});

  @override
  State<CameraMealScreen> createState() => _CameraMealScreenState();
}

class _CameraMealScreenState extends State<CameraMealScreen> {
  bool showMealResult = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      // 🔝 TOP BAR (fixed)
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: showMealResult
            ? IconButton(
                icon: const Icon(Icons.arrow_back, color: Colors.black),
                onPressed: () {
                  setState(() {
                    showMealResult = false;
                  });
                },
              )
            : IconButton(
                icon: const Icon(Icons.tune, color: Colors.black),
                onPressed: () {},
              ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_none, color: Colors.black),
            onPressed: () {},
          ),
        ],
      ),

      // 🔄 CENTER CONTENT (only this changes)
      body: AnimatedSwitcher(
        duration: const Duration(milliseconds: 250),
        child: showMealResult
            ? const MealResultContent()
            : const CameraContent(),
      ),

      // 🔻 BOTTOM BAR (fixed)
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

            // BIG CAMERA BUTTON
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
                    setState(() {
                      showMealResult = true;
                    });
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

/// ------------------
/// CAMERA CONTENT
/// ------------------
class CameraContent extends StatelessWidget {
  const CameraContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      key: const ValueKey('camera'),
      width: double.infinity,
      height: double.infinity,
      color: Colors.grey[200],
      child: const Center(
        child: Text(
          "Camera Preview",
          style: TextStyle(fontSize: 22, color: Colors.black87),
        ),
      ),
    );
  }
}

/// ------------------
/// MEAL RESULT CONTENT
/// ------------------
class MealResultContent extends StatelessWidget {
  const MealResultContent({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      key: const ValueKey('meal'),
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [

          const Text(
            "Your Meal",
            style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
          ),

          const SizedBox(height: 20),

          const Text(
            "• Shredded chicken with black beans : 1/2 cup\n"
            "  ~147 calories\n\n"
            "• Green peas: 1/4 cup\n"
            "  ~29 calories\n\n"
            "• Corn: 1/4 cup\n"
            "  ~33 calories",
            style: TextStyle(fontSize: 16),
          ),

          const SizedBox(height: 20),

          // 🖼 FOOD IMAGE (middle)
          ClipRRect(
            borderRadius: BorderRadius.circular(12),
            child: Image(
              image: AssetImage("assets/meal.jpg"),
              height: 260,
              width: double.infinity,
              fit: BoxFit.cover,
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
    );
  }
}
