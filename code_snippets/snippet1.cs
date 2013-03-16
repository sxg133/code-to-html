namespace MyNamespace {
	public class TestCodeFormatter {
		public static void Main(string[] args) {
			/*
				This program squares integers 0 through 9
			*/
			int[] squares = new int[10];
			for (int i=0; i < squares.Length; i++)
			{
				squares[i] = i * i;
			}
			string test = "Here's my \"test\" string."; // comment string
		}
	}
}