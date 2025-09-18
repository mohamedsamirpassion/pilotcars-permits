/*
 * State Regulations Database for Load Planning Feature
 * ====================================================
 * 
 * This file contains escort requirements for oversized loads across all 50 US states.
 * Original file size: 2,466 lines with complete data for all states.
 * 
 * FOR COMPLETE DATA: Copy the full state_regulations.js file from the original
 * Pilots Match project located at: static/js/state_regulations.js
 * 
 * Data Structure:
 * Each regulation object contains:
 * - state: State name
 * - road_type: "Interstate" or "Non-Interstate"  
 * - width_min/width_max: Width thresholds in feet/inches format (e.g., "12'6\"")
 * - width_escorts: Required escorts for width
 * - length_min/length_max: Length thresholds
 * - length_escorts: Required escorts for length
 * - height_min/height_max: Height thresholds
 * - height_escorts: Required escorts for height
 * - overhang_min/overhang_max: Overhang thresholds
 * - overhang_escorts: Required escorts for overhang
 * - weight_min/weight_max: Weight thresholds in pounds
 * - weight_escorts: Required escorts for weight
 * - notes: Additional requirements or restrictions
 */

const stateRegulations = [
  // ALABAMA - Sample data (copy complete data from original file)
  {
    "state": "Alabama",
    "road_type": "Interstate",
    "width_min": "12'1\"",
    "width_max": "14'0\"",
    "width_escorts": "1 Rear",
    "length_min": "90'0\"",
    "length_max": "124'11\"",
    "length_escorts": "1 Rear",
    "overhang_min": "5'1\"",
    "overhang_max": null,
    "overhang_escorts": "1 Rear",
    "height_min": "15'7\"",
    "height_max": null,
    "height_escorts": "1 High Pole",
    "notes": "Holiday travel banned >12' wide"
  },
  {
    "state": "Alabama",
    "road_type": "Non-Interstate",
    "width_min": "12'1\"",
    "width_max": "14'0\"",
    "width_escorts": "1 Front",
    "length_min": "90'0\"",
    "length_max": "124'11\"",
    "length_escorts": "1 Rear",
    "overhang_min": "5'1\"",
    "overhang_max": null,
    "overhang_escorts": "1 Rear",
    "height_min": "15'7\"",
    "height_max": null,
    "height_escorts": "1 High Pole",
    "notes": "Holiday travel banned >12' wide"
  },
  
  // FLORIDA - Sample data
  {
    "state": "Florida",
    "road_type": "Interstate",
    "width_min": "12'1\"",
    "width_max": "14'0\"",
    "width_escorts": "1 Rear",
    "length_min": "75'0\"",
    "length_max": "95'0\"",
    "length_escorts": "1 Rear depends on route",
    "overhang_min": "10'0\"",
    "overhang_max": null,
    "overhang_escorts": "1 Rear",
    "height_min": "14'7\"",
    "height_max": "15'1\"",
    "height_escorts": "1 High Pole",
    "notes": "Rush hour restrictions in urban areas"
  },
  
  // NORTH CAROLINA - Sample data
  {
    "state": "North Carolina",
    "road_type": "Interstate",
    "width_min": "12'1\"",
    "width_max": "14'0\"",
    "width_escorts": "1 Rear",
    "length_min": "110'1\"",
    "length_max": "150'0\"",
    "length_escorts": "1 Rear",
    "overhang_min": "10'0\"",
    "overhang_max": null,
    "overhang_escorts": "1 Rear",
    "height_min": "14'6\"",
    "height_max": "16'5\"",
    "height_escorts": "1 High Pole",
    "notes": "Daylight travel only >12' wide"
  },
  
  // TEXAS - Sample data
  {
    "state": "Texas",
    "road_type": "Interstate",
    "width_min": "14'1\"",
    "width_max": "16'0\"",
    "width_escorts": "1 Rear",
    "length_min": "110'1\"",
    "length_max": "125'0\"",
    "length_escorts": "1 Rear",
    "overhang_min": "10'0\"",
    "overhang_max": null,
    "overhang_escorts": "1 Rear",
    "height_min": "17'1\"",
    "height_max": "18'0\"",
    "height_escorts": "1 High Pole",
    "notes": "Daylight travel only >12' wide"
  }
  
  /*
   * IMPORTANT: This is only a sample of the data!
   * 
   * The complete file contains regulations for all 50 states with multiple rules per state.
   * To implement the full feature, you MUST copy the complete state_regulations.js file
   * from the original project.
   * 
   * The complete file includes:
   * - Alabama (6 rules)
   * - Alaska (2 rules)  
   * - Arizona (3 rules)
   * - Arkansas (10 rules)
   * - California (2 rules)
   * - Colorado (3 rules)
   * - Florida (6 rules)
   * - Georgia (4 rules)
   * - North Carolina (6 rules)
   * - South Carolina (5 rules)
   * - Tennessee (6 rules)
   * - Texas (6 rules)
   * - Virginia (2 rules)
   * - Ohio (6 rules)
   * - Pennsylvania (4 rules)
   * - New York (3 rules)
   * - New Jersey (2 rules)
   * - Illinois (2 rules)
   * - Michigan (2 rules)
   * - Indiana (2 rules)
   * - Missouri (2 rules)
   * - Wisconsin (2 rules)
   * - Minnesota (2 rules)
   * - Iowa (2 rules)
   * - Massachusetts (2 rules)
   * - Oklahoma (2 rules)
   * - Kansas (2 rules)
   * - Nebraska (2 rules)
   * - Mississippi (4 rules)
   * - Louisiana (6 rules)
   * - Connecticut (2 rules)
   * - New Hampshire (2 rules)
   * - Maine (2 rules)
   * - Hawaii (2 rules)
   * - Maryland (2 rules)
   * - Delaware (2 rules)
   * - West Virginia (8 rules)
   * - Kentucky (6 rules)
   * - New Mexico (6 rules)
   * - Rhode Island (1 rule)
   * 
   * Total: 130+ regulation rules across all states
   */
];
